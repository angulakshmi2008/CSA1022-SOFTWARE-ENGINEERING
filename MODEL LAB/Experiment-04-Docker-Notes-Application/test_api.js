/**
 * Automated REST API Test Suite for Q4: Notes Express Application
 * Can test a running server or start an in-process instance on an ephemeral port.
 */

const http = require('http');
const { app } = require('./server');

const TEST_PORT = 3001;
let server;

function makeRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const payload = body ? JSON.stringify(body) : null;
    const options = {
      hostname: '127.0.0.1',
      port: TEST_PORT,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...(payload ? { 'Content-Length': Buffer.byteLength(payload) } : {})
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode, headers: res.headers, body: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, headers: res.headers, body: data });
        }
      });
    });

    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

async function runTests() {
  console.log("==================================================================");
  console.log(" STARTING AUTOMATED REST API TEST SUITE (Node.js Express Notes App)");
  console.log("==================================================================");

  let passed = 0;
  let failed = 0;

  function assert(condition, testName, details = "") {
    if (condition) {
      console.log(`[PASS] ${testName}`);
      passed++;
    } else {
      console.error(`[FAIL] ${testName} ${details ? '--> ' + details : ''}`);
      failed++;
    }
  }

  // Start test server
  await new Promise((resolve) => {
    server = app.listen(TEST_PORT, '127.0.0.1', resolve);
  });

  try {
    // Test 1: GET / - Health Check
    const resHealth = await makeRequest('GET', '/');
    assert(resHealth.status === 200, "Test 1: GET / returns HTTP 200 OK");
    assert(resHealth.body.status === "UP", "Test 1b: GET / status is 'UP'");

    // Test 2: GET /notes - List notes initial
    const resNotesInit = await makeRequest('GET', '/notes');
    assert(resNotesInit.status === 200, "Test 2: GET /notes returns HTTP 200 OK");
    assert(Array.isArray(resNotesInit.body.notes), "Test 2b: GET /notes returns array of notes");
    const initialCount = resNotesInit.body.count;

    // Test 3: POST /notes - Add valid note
    const validPayload = {
      title: "Sprint Review Notes",
      content: "Discuss user stories and pull request code review best practices."
    };
    const resPostValid = await makeRequest('POST', '/notes', validPayload);
    assert(resPostValid.status === 201, "Test 3: POST /notes valid returns HTTP 201 Created");
    assert(resPostValid.body.note && resPostValid.body.note.id, "Test 3b: POST /notes returns created note with ID");
    assert(resPostValid.body.note.title === "Sprint Review Notes", "Test 3c: POST /notes title matches payload");
    const createdId = resPostValid.body.note.id;

    // Test 4: POST /notes - Invalid note (Empty content)
    const emptyPayload = { title: "Empty Note", content: "" };
    const resPostEmpty = await makeRequest('POST', '/notes', emptyPayload);
    assert(resPostEmpty.status === 400, "Test 4: POST /notes empty content returns HTTP 400 Bad Request");
    assert(resPostEmpty.body.message.includes("content is required"), "Test 4b: Error message clarifies content required");

    // Test 5: POST /notes - Invalid note (Whitespace-only content)
    const whitespacePayload = { title: "Space Note", content: "     " };
    const resPostSpace = await makeRequest('POST', '/notes', whitespacePayload);
    assert(resPostSpace.status === 400, "Test 5: POST /notes whitespace content returns HTTP 400 Bad Request");

    // Test 6: POST /notes - Missing content field entirely
    const missingPayload = { title: "No Content Note" };
    const resPostMissing = await makeRequest('POST', '/notes', missingPayload);
    assert(resPostMissing.status === 400, "Test 6: POST /notes missing content key returns HTTP 400 Bad Request");

    // Test 7: GET /notes after addition - verify persistence in memory
    const resNotesAfter = await makeRequest('GET', '/notes');
    assert(resNotesAfter.body.count === initialCount + 1, "Test 7: GET /notes shows count increased by 1");
    const foundNote = resNotesAfter.body.notes.find(n => n.id === createdId);
    assert(!!foundNote, "Test 7b: Newly created note is present in notes list");

    // Test 8: GET /notes/:id
    const resGetSingle = await makeRequest('GET', `/notes/${createdId}`);
    assert(resGetSingle.status === 200, "Test 8: GET /notes/:id returns HTTP 200");
    assert(resGetSingle.body.id === createdId, "Test 8b: GET /notes/:id matches requested ID");

    // Test 9: DELETE /notes/:id
    const resDelete = await makeRequest('DELETE', `/notes/${createdId}`);
    assert(resDelete.status === 200, "Test 9: DELETE /notes/:id returns HTTP 200 OK");

    console.log("==================================================================");
    console.log(` TEST SUMMARY: ${passed} PASSED | ${failed} FAILED`);
    console.log("==================================================================");

    if (failed > 0) process.exit(1);

  } catch (err) {
    console.error("Test execution failed with unexpected error:", err);
    process.exit(1);
  } finally {
    server.close();
  }
}

if (require.main === module) {
  runTests();
}

module.exports = { runTests };
