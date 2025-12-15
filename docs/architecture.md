# Backend Architecture

## Overview
The backend of StudIA is built using FastAPI and follows a modular, service-oriented architecture. This design ensures scalability, maintainability, and clear separation of concerns.

## Proposed Structure
```
backend/
    app/
        models/          # Database models
        routes/          # API endpoints
        services/        # Business logic
            generative/  # AI-related services
            pdf_parser/  # PDF parsing services
            relational_db_manager/  # Relational DB management
            vector_db_manager/      # Vector DB management
        utils/           # Utility functions (e.g., logging, error handling)
        tests/           # Unit and integration tests
```

### Key Improvements
1. **Utils Folder**:
   - Centralize shared utilities like logging and error handling.
2. **Service Refactoring**:
   - Ensure each service adheres to the single responsibility principle.
   - Use dependency injection for better testability.
3. **Database Management**:
   - Refactor `vector_db_manager` to ensure compatibility with the latest Milvus version.
   - Standardize database operations across services.

### Detailed Components
- **Models**: Define Pydantic models for data validation and serialization.
- **Routes**: Implement RESTful endpoints for interacting with the frontend.
- **Services**: Encapsulate business logic, including AI generation, database management, and file parsing.
- **Utils**: Provide reusable utilities for logging, configuration, and error handling.
- **Tests**: Ensure code quality with unit and integration tests.

---

# Frontend Architecture

## Overview
The frontend of StudIA is built using Angular. The proposed structure emphasizes modularity and state management to handle complex data flows efficiently.

## Proposed Structure
```
frontend/
    src/
        app/
            components/  # Reusable components
            pages/       # Page-level components (e.g., dashboard, file upload)
            services/    # API services for backend communication
            models/      # TypeScript interfaces/models
            utils/       # Shared utilities
```

### Key Improvements
1. **Modular Components**:
   - Separate reusable components from page-level components.
2. **State Management**:
   - Use NgRx for managing application state.
3. **API Services**:
   - Centralize backend communication in dedicated services.

### Detailed Components
- **Components**: Build reusable UI elements.
- **Pages**: Develop page-specific components for user interactions.
- **Services**: Handle API calls and data transformations.
- **Models**: Define TypeScript interfaces for type safety.
- **Utils**: Implement shared utilities for common tasks.

---

This architecture ensures a clean separation of concerns, making the codebase easier to maintain and scale.