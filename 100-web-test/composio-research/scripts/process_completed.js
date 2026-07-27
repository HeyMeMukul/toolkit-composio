const fs = require('fs');
const queuePath = 'data/state/task_queue.json';
const queue = JSON.parse(fs.readFileSync(queuePath, 'utf8'));

const completedIds = process.argv.slice(2);
completedIds.forEach(id => {
    if (queue[id]) {
        queue[id].status = 'completed';
    }
});

const pending = Object.keys(queue).filter(id => queue[id].status === 'pending');
const nextBatchIds = pending.slice(0, 5);
const nextBatch = [];

if (nextBatchIds.length > 0) {
    nextBatchIds.forEach(id => {
        queue[id].status = 'in-progress';
        nextBatch.push({id, ...queue[id]});
    });
}

fs.writeFileSync(queuePath, JSON.stringify(queue, null, 2));
console.log(JSON.stringify(nextBatch));
