# Frontend Architecture

## Overview
The frontend will be rebuilt using **Next.js** and **TypeScript**. This choice ensures server-side rendering (SSR) for better performance and SEO, while TypeScript provides type safety and scalability.

---

## Proposed Structure
```
frontend/
    src/
        components/      # Reusable UI components
        pages/           # Next.js pages (routes)
        services/        # API services for backend communication
        models/          # TypeScript interfaces/models
        utils/           # Shared utilities
        styles/          # Global and modular styles
```

### Key Features
1. **Server-Side Rendering (SSR)**:
   - Use Next.js’s SSR capabilities for dynamic content.
2. **TypeScript**:
   - Ensure type safety and reduce runtime errors.
3. **API Integration**:
   - Centralize API calls in `services/`.
4. **Modular Components**:
   - Build reusable components for consistency and maintainability.
5. **Styling**:
   - Use CSS modules or styled-components for scoped styles.

---

## Detailed Components

### 1. **Components**
- Purpose: Reusable UI elements (e.g., buttons, modals).
- Location: `src/components/`

### 2. **Pages**
- Purpose: Define routes and page-level components.
- Location: `src/pages/`
- Example:
  - `src/pages/index.tsx`: Home page.
  - `src/pages/dashboard.tsx`: User dashboard.

### 3. **Services**
- Purpose: Handle API communication with the backend.
- Location: `src/services/`
- Example:
  - `src/services/api.ts`: Centralized API client using Axios or Fetch.

### 4. **Models**
- Purpose: Define TypeScript interfaces for data structures.
- Location: `src/models/`
- Example:
  - `src/models/User.ts`: Interface for user data.

### 5. **Utils**
- Purpose: Shared utility functions (e.g., formatters, validators).
- Location: `src/utils/`

### 6. **Styles**
- Purpose: Define global and modular styles.
- Location: `src/styles/`
- Example:
  - `src/styles/global.css`: Global styles.
  - `src/styles/Button.module.css`: Scoped styles for components.

---

## Next Steps
1. Set up a new Next.js project:
   ```bash
   npx create-next-app@latest frontend --typescript
   ```
2. Define the folder structure as outlined above.
3. Implement core pages and components.
4. Integrate with the backend APIs.
5. Add unit and integration tests using Jest and React Testing Library.

This architecture ensures a modern, scalable, and maintainable frontend for StudIA.