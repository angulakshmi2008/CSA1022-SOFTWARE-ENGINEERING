/**
 * Q4: Node.js Express Notes REST API
 * Designed for Containerization with Docker
 *
 * Requirements:
 * - GET /       : Health check & API info
 * - GET /notes  : List all notes
 * - POST /notes : Add a new note with validation (content required, non-empty)
 */

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON request bodies
app.use(express.json());

// In-Memory Storage for Notes
// Note: In-memory arrays reside in container RAM and reset when container restarts/removes.
let notes = [
  {
    id: 1,
    title: "Lab Practical Requirement",
    content: "Complete Software Engineering Model Practical Set 2 deliverables.",
    createdAt: new Date().toISOString()
  },
  {
    id: 2,
    title: "Docker Containerization",
    content: "Build and run the Node.js Express application inside Docker container.",
    createdAt: new Date().toISOString()
  }
];

let nextId = 3;

// 1. Root / Health Check Endpoint
app.get('/', (req, res) => {
  res.status(200).json({
    status: "UP",
    application: "Notes REST API",
    version: "1.0.0",
    message: "Server is healthy and ready to handle requests.",
    containerEnvironment: process.env.IS_DOCKER ? "Docker Container" : "Host System",
    timestamp: new Date().toISOString()
  });
});

// 2. GET /notes - Retrieve all notes
app.get('/notes', (req, res) => {
  res.status(200).json({
    count: notes.length,
    notes: notes
  });
});

// 3. GET /notes/:id - Retrieve a specific note by ID
app.get('/notes/:id', (req, res) => {
  const noteId = parseInt(req.params.id, 10);
  const note = notes.find(n => n.id === noteId);

  if (!note) {
    return res.status(404).json({
      error: "Not Found",
      message: `Note with ID ${noteId} does not exist.`
    });
  }

  res.status(200).json(note);
});

// 4. POST /notes - Add a new note with validation
app.post('/notes', (req, res) => {
  const { title, content } = req.body;

  // Validation: Content is strictly required and cannot be empty or whitespace
  if (!content || typeof content !== 'string' || content.trim().length === 0) {
    return res.status(400).json({
      error: "Bad Request",
      message: "Note content is required and cannot be empty."
    });
  }

  const newNote = {
    id: nextId++,
    title: (title && typeof title === 'string' && title.trim().length > 0) ? title.trim() : "Untitled Note",
    content: content.trim(),
    createdAt: new Date().toISOString()
  };

  notes.push(newNote);

  res.status(201).json({
    message: "Note added successfully.",
    note: newNote
  });
});

// 5. DELETE /notes/:id - Remove a note (useful for test cleanup)
app.delete('/notes/:id', (req, res) => {
  const noteId = parseInt(req.params.id, 10);
  const index = notes.findIndex(n => n.id === noteId);

  if (index === -1) {
    return res.status(404).json({
      error: "Not Found",
      message: `Note with ID ${noteId} does not exist.`
    });
  }

  const removed = notes.splice(index, 1)[0];
  res.status(200).json({
    message: "Note deleted successfully.",
    deletedNote: removed
  });
});

// Start Server if run directly
let serverInstance = null;
if (require.main === module) {
  serverInstance = app.listen(PORT, '0.0.0.0', () => {
    console.log(`====================================================`);
    console.log(` Notes Express API listening on http://0.0.0.0:${PORT}`);
    console.log(` Ready for HTTP client & Docker container requests`);
    console.log(`====================================================`);
  });
}

// Export for programmatic testing
module.exports = { app, notes };
