#!/usr/bin/env node
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import prompts from 'prompts';
import pc from 'picocolors';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function init() {
  console.log(pc.cyan(pc.bold('\n🚀 Welcome to OpenCode Workspace Scaffold CLI!\n')));

  const response = await prompts([
    {
      type: 'select',
      name: 'template',
      message: 'Which OpenCode workspace template would you like to use?',
      choices: [
        { title: 'Content Creator (Blog, Social Media, Audits)', value: 'content-creator' }
        // Add more templates here in the future
      ],
    },
    {
      type: 'text',
      name: 'projectName',
      message: 'Project name:',
      initial: 'my-opencode-workspace'
    }
  ]);

  if (!response.template || !response.projectName) {
    console.log(pc.red('❌ Initialization cancelled.'));
    process.exit(1);
  }

  const targetDir = path.resolve(process.cwd(), response.projectName);
  const templateDir = path.resolve(__dirname, '../templates', response.template);

  if (fs.existsSync(targetDir)) {
    console.log(pc.red(`\n❌ Error: Directory "${response.projectName}" already exists.`));
    process.exit(1);
  }

  console.log(pc.blue(`\n📂 Creating workspace in ${targetDir}...`));
  
  try {
    await fs.copy(templateDir, targetDir);
    
    console.log(pc.green(pc.bold('\n✅ Workspace successfully created!')));
    console.log(pc.white(`\nNext steps:`));
    console.log(pc.cyan(`  cd ${response.projectName}`));
    console.log(pc.cyan(`  opencode\n`));
  } catch (err) {
    console.error(pc.red('\n❌ Failed to copy template files:'), err);
  }
}

init().catch((e) => {
  console.error(e);
  process.exit(1);
});
