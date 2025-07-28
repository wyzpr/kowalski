#!/usr/bin/env node
import chalk from 'chalk';
import inquirer from 'inquirer';
import gradient from 'gradient-string';
import chalkAnimation from 'chalk-animation';
import figlet from 'figlet';
import { createSpinner } from 'nanospinner';

let playerName;
const sleep = (ms = 2000) => new Promise((r) => setTimeout(r, ms)); //Function to sleep for given time


async function askName() {
    const answer = await inquirer.prompt({
        name: 'player_name',
        type: 'input',
        message: 'What is your name?',
        default() {
            return 'Player';
        },
    });
    playerName = answer.player_name;
}


async function delt3Intro() {
    const title = chalkAnimation.rainbow("It's T! V! TIME!\n");
    await sleep();
    title.stop();

    console.log(`
    ${chalk.blueBright('WELCOME TO MY WORLD!')} 
    I am Tenna, a high-budget, souped-up version of Mettaton!
    (if you get any questions wrong, say ${chalk.bgRed('G O O D B Y E.')})
  `);

}

async function handleAnswer(isCorrect) {
    const spinner = createSpinner('Checking answer...').start();
    await sleep();

    if (isCorrect) {
        spinner.success({ text: `Nice work ${playerName}. You live on... `});
    } else {
        spinner.error({text:`You FOOL. Die, ${playerName}.`});
        process.exit(1);
    }
}

async function q1() {
    const answer = await inquirer.prompt({
        name: 'question',
        type: 'list',
        message: 'Undertale was launched in: ',
        choices: ['2009','2011','"2015"','2015'],
    });
    return handleAnswer(answer.question == '2015');
}



await delt3Intro();
await askName();
await q1();