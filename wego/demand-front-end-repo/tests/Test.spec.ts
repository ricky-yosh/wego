// import { test, expect } from '@playwright/test';
import { test, expect} from '@playwright/test';

// Function to generate a random string
function generateRandomString(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

// Function to generate a random email
function generateRandomEmail() {
  const username = generateRandomString(8);
  return `${username}@example.com`;
}

let randomUsername;
let randomEmail;
let randomPassword;

test.describe('User flow', () => {

  randomUsername = generateRandomString(8);
    randomEmail = generateRandomEmail();
    randomPassword = generateRandomString(10)

  test('redirects to login from home if not authenticated', async ({ page }) => {
    await page.goto('https://team-12.seuswe.rocks');
    await expect(page).toHaveURL('https://team-12.seuswe.rocks/login');
  });

  test('navigates to sign up page when click on sign up', async ({ page }) => {
    await page.goto('https://team-12.seuswe.rocks/login');
    await page.click('text=Sign Up');
    await expect(page).toHaveURL('https://team-12.seuswe.rocks/signup');
  });

  test('allows user to sign up', async ({ page }) => {
    await page.goto('https://team-12.seuswe.rocks/signup');
    

    await page.goto('https://team-12.seuswe.rocks/signup');
    await page.fill('input[name="username"]', randomUsername);
    await page.fill('input[name="email"]', randomEmail);
    await page.fill('input[name="password"]', randomPassword);
    await page.fill('input[name="confirmPassword"]', randomPassword);
    await page.click('text=Sign Up');
    
   
  });

  test('allows user to log in and redirects to home', async ({ page }) => {
    await page.goto('https://team-12.seuswe.rocks/login');
    await page.fill('input[name="username"]', randomUsername);
    await page.fill('input[name="password"]', randomPassword);
    await page.click('text=Login');

  
    await expect(page).toHaveTitle("WeGo");

    
  });

  

});
