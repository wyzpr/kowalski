#!/usr/bin/env node

import { program } from 'commander';
import chalk from 'chalk';

program
  .name('mycli')
  .description('Translate a sentence to a specific language')
  .version('1.0.0')
  .option('-l, --language <lang>', 'Language to translate to')
  .option('-s, --sentence <text>', 'Sentence to translate')
  .action((options) => {
    const { language, sentence } = options;
    console.log(chalk.green(`Translating to ${language}: "${sentence}"`));
  });

program.parse();