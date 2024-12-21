import fs from 'node:fs';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

let num = 0;

const saveScrenShot = (data: string | NodeJS.ArrayBufferView) => {
    const filePath = `${process.cwd()}/scs${num}.png`; // 使用當前工作目錄
    fs.writeFileSync(filePath, data);
    console.log(`Screenshot saved to: ${filePath}`);
    num++;
}


interface pwd_id {
    id: string
    pwd: string
}
const pwd_id_ready = ({ id, pwd }: pwd_id) => {
    return (Boolean(pwd.length) && Boolean(id.length))
}

export {
    delay,
    saveScrenShot,
    pwd_id_ready
}
