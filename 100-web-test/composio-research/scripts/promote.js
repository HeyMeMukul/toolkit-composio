const fs = require('fs');
const path = require('path');

const rawDir = 'data/raw';
const verifiedDir = 'data/verified';

if (!fs.existsSync(verifiedDir)) {
    fs.mkdirSync(verifiedDir, { recursive: true });
}

const rawFiles = fs.readdirSync(rawDir).filter(f => f.endsWith('.json'));

let promotedCount = 0;

for (const file of rawFiles) {
    const verifiedPath = path.join(verifiedDir, file);
    if (!fs.existsSync(verifiedPath)) {
        const rawContent = fs.readFileSync(path.join(rawDir, file), 'utf8');
        const appData = JSON.parse(rawContent);
        appData.confidence = "agent_only";
        fs.writeFileSync(verifiedPath, JSON.stringify(appData, null, 2));
        promotedCount++;
    }
}

console.log(`Promoted ${promotedCount} unverified apps to data/verified/ with confidence="agent_only".`);
