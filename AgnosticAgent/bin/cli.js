#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// ─── Renkli Çıktı ─────────────────────────────────────
const c = {
    green: (t) => `\x1b[32m${t}\x1b[0m`,
    yellow: (t) => `\x1b[33m${t}\x1b[0m`,
    red: (t) => `\x1b[31m${t}\x1b[0m`,
    cyan: (t) => `\x1b[36m${t}\x1b[0m`,
    bold: (t) => `\x1b[1m${t}\x1b[0m`,
    dim: (t) => `\x1b[2m${t}\x1b[0m`,
};

// ─── Yardım ────────────────────────────────────────────
function printHelp() {
    console.log(`
${c.bold('🚀 Agent Prompt System — Proje Oluşturucu')}

${c.cyan('Kullanım:')}
  npx create-agent-system <proje-adı>
  npx create-agent-system .              ${c.dim('(mevcut dizine kur)')}

${c.cyan('Örnekler:')}
  npx create-agent-system my-saas-app
  npx create-agent-system ./existing-project

${c.cyan('Seçenekler:')}
  --help, -h     Bu yardım mesajını gösterir
  --no-git       Git init ve hooks kurulumunu atlar
  --verbose      Detaylı çıktı gösterir
`);
}

// ─── Dosya Kopyalama (Recursive) ───────────────────────
function copyDirSync(src, dest, verbose = false) {
    let count = 0;

    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            count += copyDirSync(srcPath, destPath, verbose);
        } else {
            fs.copyFileSync(srcPath, destPath);
            count++;
            if (verbose) {
                console.log(c.dim(`  → ${path.relative(dest, destPath)}`));
            }
        }
    }

    return count;
}

// ─── Ana Fonksiyon ─────────────────────────────────────
function main() {
    const args = process.argv.slice(2);

    // Flags
    const help = args.includes('--help') || args.includes('-h');
    const noGit = args.includes('--no-git');
    const verbose = args.includes('--verbose');

    // Proje adı (flag olmayanlar)
    const positional = args.filter((a) => !a.startsWith('--') && !a.startsWith('-'));
    const projectName = positional[0];

    if (help || !projectName) {
        printHelp();
        process.exit(help ? 0 : 1);
    }

    // ─── Hedef dizin belirleme ──────────────────────────
    const targetDir = path.resolve(process.cwd(), projectName);
    const isCurrent = projectName === '.';
    const displayName = isCurrent ? path.basename(targetDir) : projectName;

    console.log('');
    console.log(c.bold('🚀 Agent Prompt System'));
    console.log(c.dim(`   Proje: ${displayName}`));
    console.log(c.dim(`   Hedef: ${targetDir}`));
    console.log('');

    // ─── Hedef dizin kontrolü ───────────────────────────
    if (!isCurrent && fs.existsSync(targetDir)) {
        const contents = fs.readdirSync(targetDir);
        if (contents.length > 0) {
            console.log(c.red(`❌ Hata: "${projectName}" dizini zaten var ve boş değil.`));
            console.log(c.dim('   Boş bir dizin veya yeni bir isim kullanın.'));
            process.exit(1);
        }
    }

    // Hedef dizini oluştur
    if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
    }

    // ─── Template dosyalarını kopyala ───────────────────
    const templateDir = path.join(__dirname, '..', 'template');

    if (!fs.existsSync(templateDir)) {
        console.log(c.red('❌ Template dizini bulunamadı!'));
        console.log(c.dim(`   Beklenen konum: ${templateDir}`));
        process.exit(1);
    }

    console.log('📦 Template dosyaları kopyalanıyor...');
    const fileCount = copyDirSync(templateDir, targetDir, verbose);
    console.log(c.green(`   ✅ ${fileCount} dosya kopyalandı`));

    // ─── Çalıştırılabilir izinleri ayarla ───────────────
    const executableFiles = [
        '.agent/hooks/pre-commit',
        '.agent/hooks/install.sh',
    ];

    for (const relPath of executableFiles) {
        const fullPath = path.join(targetDir, relPath);
        if (fs.existsSync(fullPath)) {
            try {
                fs.chmodSync(fullPath, 0o755);
            } catch {
                // Windows'ta chmod çalışmaz, sessizce geç
            }
        }
    }

    // ─── Git init + hooks ───────────────────────────────
    if (!noGit) {
        const { execSync } = require('child_process');
        const gitDir = path.join(targetDir, '.git');

        if (!fs.existsSync(gitDir)) {
            console.log('');
            console.log('📂 Git repository oluşturuluyor...');
            try {
                execSync('git init', { cwd: targetDir, stdio: 'pipe' });
                console.log(c.green('   ✅ git init tamamlandı'));
            } catch {
                console.log(c.yellow('   ⚠️  git init başarısız (git yüklü mü?)'));
            }
        }

        // Git hooks kurulumu
        const installScript = path.join(targetDir, '.agent', 'hooks', 'install.sh');
        if (fs.existsSync(installScript) && fs.existsSync(path.join(targetDir, '.git'))) {
            console.log('🔗 Git hooks kuruluyor...');
            try {
                execSync(`bash "${installScript}"`, { cwd: targetDir, stdio: 'pipe' });
                console.log(c.green('   ✅ Pre-commit hook kuruldu'));
            } catch {
                console.log(c.yellow('   ⚠️  Hook kurulumu başarısız (bash yüklü mü?)'));
            }
        }
    }

    // ─── .gitignore oluştur (yoksa) ─────────────────────
    const gitignorePath = path.join(targetDir, '.gitignore');
    if (!fs.existsSync(gitignorePath)) {
        const gitignoreContent = [
            'node_modules/',
            '.env',
            '.env.local',
            '.DS_Store',
            '',
            '# Agent System',
            '.agent/cache/',
            '.agent/state/',
            '.agent/logs/',
            '.agent/backups/',
            'docs/project_keys.md',
            '',
        ].join('\n');

        fs.writeFileSync(gitignorePath, gitignoreContent);
        console.log(c.green('   ✅ .gitignore oluşturuldu'));
    }

    // ─── Başarı mesajı ──────────────────────────────────
    console.log('');
    console.log(c.green(c.bold('🎉 Agent Prompt System kuruldu!')));
    console.log('');
    console.log(c.cyan('Sonraki adımlar:'));

    if (!isCurrent) {
        console.log(`  ${c.bold('1.')} cd ${projectName}`);
        console.log(`  ${c.bold('2.')} python3 .agent/scripts/core/health_check.py`);
        console.log(`  ${c.bold('3.')} Agent'a ${c.bold('/start')} komutunu ver`);
    } else {
        console.log(`  ${c.bold('1.')} python3 .agent/scripts/core/health_check.py`);
        console.log(`  ${c.bold('2.')} Agent'a ${c.bold('/start')} komutunu ver`);
    }

    console.log('');
    console.log(c.dim('Detaylı kullanım: README.md'));
    console.log('');
}

main();
