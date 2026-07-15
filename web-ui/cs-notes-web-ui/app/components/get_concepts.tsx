"use server"

import * as dotenv from 'dotenv'
import * as fs from 'fs';

dotenv.config({ path: "../../../../.env"}) // this is bad, but just don't touch it

export async function test_file() {
  console.log(process.env.CONCEPTS_TXT_FILE!)
  fs.readFileSync(process.env.CONCEPTS_TXT_FILE!, 'utf-8');
}