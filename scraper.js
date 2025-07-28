import {load} from 'cheerio';

(async () => {
  const url = 'https://www.example.com';
  const response = await fetch(url);

  const $ = load(await response.text());
  //console.log($.html());

  const text = $('p').text();
  console.log(text);
})();