const fs = require('fs');
const path = require('path');

const rawDir = 'data/raw';
const files = fs.readdirSync(rawDir).filter(f => f.endsWith('.json'));

const categories = {};
const apps = [];

// Read all apps
files.forEach(file => {
    const content = fs.readFileSync(path.join(rawDir, file), 'utf8');
    const app = JSON.parse(content);
    apps.push(app);
    
    if (!categories[app.category]) {
        categories[app.category] = [];
    }
    categories[app.category].push(app.app_id);
});

const sampleIds = new Set();

// 1. Stratified sample (2 per category randomly)
for (const category in categories) {
    const ids = categories[category];
    // Shuffle ids
    for (let i = ids.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [ids[i], ids[j]] = [ids[j], ids[i]];
    }
    // Take 2
    ids.slice(0, 2).forEach(id => sampleIds.add(id));
}

// 2. Add uncertain records
apps.forEach(app => {
    let uncertain = false;
    
    // Check fields for "unknown"
    const checkUnknown = (obj) => {
        if (typeof obj === 'string' && obj.toLowerCase().includes('unknown')) {
            uncertain = true;
        } else if (typeof obj === 'object' && obj !== null) {
            for (const key in obj) {
                checkUnknown(obj[key]);
            }
        }
    };
    checkUnknown(app);
    
    if (uncertain) {
        sampleIds.add(app.app_id);
    }
});

console.log(JSON.stringify(Array.from(sampleIds)));
