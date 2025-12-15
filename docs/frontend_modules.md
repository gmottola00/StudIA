# Frontend Modules

## Overview
The frontend of StudIA, built with Next.js and TypeScript, is divided into modular components and services. This document outlines the purpose, inputs, outputs, and interactions of each module.

---

## Modules

### 1. **File Upload Component**
- **Purpose**: Allow users to upload PDF and audio files.
- **Inputs**: Files (PDF, audio).
- **Outputs**: File metadata sent to the backend.
- **Interactions**:
  - Communicates with the backend file upload API.
  - Provides a drag-and-drop interface for users.

### 2. **Dashboard Component**
- **Purpose**: Display uploaded files and AI-generated outputs.
- **Inputs**: User data and AI outputs.
- **Outputs**: Rendered dashboard view.
- **Interactions**:
  - Fetches data from backend APIs.
  - Displays file history and AI-generated content.

### 3. **AI Output Viewer**
- **Purpose**: Display AI-generated content (e.g., summaries, flashcards).
- **Inputs**: AI-generated data.
- **Outputs**: Rendered content (text, cards, quizzes).
- **Interactions**:
  - Dynamically renders content based on user selection.

### 4. **Authentication Module**
- **Purpose**: Handle user login and registration.
- **Inputs**: User credentials.
- **Outputs**: Authentication tokens.
- **Interactions**:
  - Communicates with the backend authentication API.
  - Stores tokens in local storage or cookies.

### 5. **API Service**
- **Purpose**: Centralize API communication.
- **Inputs**: API requests.
- **Outputs**: API responses.
- **Interactions**:
  - Handles all backend communication (e.g., file upload, AI generation).
  - Uses Axios or Fetch for HTTP requests.

### 6. **State Management**
- **Purpose**: Manage application state.
- **Inputs**: User actions and API responses.
- **Outputs**: Updated state.
- **Interactions**:
  - Uses a state management library (e.g., Redux, Zustand).
  - Shares state across components.

---

## Next Steps
1. Implement each module in the `src/` folder.
2. Write unit tests for all components and services.
3. Ensure seamless integration with the backend.

This modular approach ensures a scalable and maintainable frontend architecture.