"use server"

import * as fs from 'fs';

export async function test_file() {
  console.log(process.env.CONCEPTS_TXT_FILE!)
  fs.readFileSync(process.env.CONCEPTS_TXT_FILE!, 'utf-8');
}