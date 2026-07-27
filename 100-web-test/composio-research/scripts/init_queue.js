const fs = require('fs');
const apps = JSON.parse(fs.readFileSync('data/apps_list.json', 'utf8'));
const queue = {};
for (const app of apps) {
    queue[app.id] = {
        status: 'pending',
        name: app.name,
        category: app.category,
        website: app.website,
        retries: 0
    };
}
fs.writeFileSync('data/state/task_queue.json', JSON.stringify(queue, null, 2));
console.log('Task queue initialized.');
