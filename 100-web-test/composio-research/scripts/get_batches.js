const fs = require('fs');
const queuePath = 'data/state/task_queue.json';
const queue = JSON.parse(fs.readFileSync(queuePath, 'utf8'));

const pending = Object.keys(queue).filter(id => queue[id].status === 'pending');
const batches = [];
for (let i = 0; i < 5; i++) {
    const batchIds = pending.slice(i * 5, (i + 1) * 5);
    if (batchIds.length > 0) {
        const batch = batchIds.map(id => ({id, ...queue[id]}));
        batches.push(batch);
        batchIds.forEach(id => {
            queue[id].status = 'in-progress';
        });
    }
}
fs.writeFileSync(queuePath, JSON.stringify(queue, null, 2));
console.log(JSON.stringify(batches));
