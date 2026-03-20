# Development Walkthroughs

## Complete Step-by-Step Guides for Real-World Projects

This guide provides detailed, step-by-step instructions for building three different types of applications using the Kiro-CLI Agent Team System. Each walkthrough demonstrates the systematic approach and agent coordination patterns for different project types.

---

## 🌟 Walkthrough 1: Greenfield Fullstack Application

**Project**: Task Management SaaS Platform  
**Tech Stack**: React + TypeScript + Node.js + PostgreSQL  
**Timeline**: 2-3 weeks  
**Complexity**: High

### Phase 1: Project Initialization and Planning

#### Step 1: Start Project Planning
```bash
# Type this in your terminal or chat:
@prime
```

**What happens**: Project Manager loads comprehensive project context and begins systematic planning.

**You'll be asked questions like**:
- What type of application are you building?
- Who are your target users?
- What are the core features needed?
- What's your timeline and team size?

**Your responses** (example):
```
Application Type: Task Management SaaS Platform
Target Users: Small to medium businesses (10-100 employees)
Core Features: 
- User authentication and team management
- Task creation, assignment, and tracking
- Project organization and dashboards
- Real-time collaboration and notifications
- Reporting and analytics
Timeline: 3 weeks for MVP
Team: Solo developer with AI agent assistance
```

#### Step 2: Create Comprehensive Feature Plan
```bash
@plan-feature "Task Management SaaS MVP"
```

**What happens**: Project Manager creates detailed implementation plan with task breakdown.

**Expected output**: Comprehensive project plan with:
- Feature breakdown and user stories
- Technical architecture recommendations
- Development phases and milestones
- Agent assignment and coordination plan

#### Step 3: Generate Product Requirements Document
```bash
@create-prd "Task Management SaaS Platform"
```

**What happens**: Project Manager creates formal PRD with business requirements, technical specifications, and success criteria.

### Phase 2: Database Design and Setup

#### Step 4: Design Database Schema
```bash
# Switch to Database Specialist
Database Specialist, I need to design a database schema for a task management SaaS platform with users, teams, projects, tasks, and real-time collaboration features.
```

**What happens**: Database Specialist asks clarifying questions about:
- Data relationships and constraints
- Performance requirements
- Scalability needs
- Compliance requirements

#### Step 5: Execute Database Implementation
```bash
@execute
```

**What happens**: Database Specialist systematically:
- Designs normalized schema with proper relationships
- Creates migration scripts with rollback procedures
- Sets up indexes for optimal query performance
- Implements data validation and constraints
- Creates test data fixtures

**Expected deliverables**:
- Complete PostgreSQL schema
- Migration scripts in `database/migrations/`
- Schema documentation
- Performance optimization plan

### Phase 3: Backend API Development

#### Step 6: Design Backend Architecture
```bash
# Switch to Backend Engineer
Backend Engineer, I need to build a REST API for the task management platform with JWT authentication, real-time features, and integration with the PostgreSQL database designed by the Database Specialist.
```

**What happens**: Backend Engineer analyzes requirements and asks about:
- API design patterns and endpoints needed
- Authentication and authorization requirements
- Real-time features and WebSocket needs
- Performance and scalability requirements

#### Step 7: Execute Backend Implementation
```bash
@execute
```

**What happens**: Backend Engineer systematically implements:
- Express.js server with TypeScript
- JWT-based authentication system
- RESTful API endpoints for all entities
- WebSocket integration for real-time updates
- Input validation with Zod
- Comprehensive error handling
- API documentation with Swagger

**Expected deliverables**:
- Complete Node.js/Express API in `backend/`
- Authentication middleware and JWT handling
- All CRUD endpoints for users, teams, projects, tasks
- Real-time WebSocket implementation
- API documentation and testing endpoints

### Phase 4: Frontend Application Development

#### Step 8: Design Frontend Architecture
```bash
# Switch to Frontend Architect
Frontend Architect, I need to build a modern React application for the task management SaaS platform. It should have a professional dashboard interface, real-time updates, and excellent user experience.
```

**What happens**: Frontend Architect asks about:
- Design preferences and branding requirements
- User experience priorities and workflows
- Device support and responsive design needs
- Performance and accessibility requirements

#### Step 9: Execute Frontend Implementation
```bash
@execute
```

**What happens**: Frontend Architect systematically builds:
- React application with TypeScript
- Modern component architecture with atomic design
- Redux Toolkit for state management
- RTK Query for API integration
- Real-time WebSocket integration
- Responsive design with Tailwind CSS
- Comprehensive routing and navigation

**Expected deliverables**:
- Complete React application in `frontend/`
- Professional dashboard and task management UI
- Real-time collaboration features
- Mobile-responsive design
- User authentication flows

### Phase 5: Quality Assurance and Testing

#### Step 10: Implement Comprehensive Testing
```bash
# Switch to Test Orchestrator
Test Orchestrator, I need to implement comprehensive testing for the fullstack task management application, including unit tests, integration tests, and end-to-end testing.
```

#### Step 11: Execute Testing Implementation
```bash
@execute
```

**What happens**: Test Orchestrator systematically creates:
- Unit tests for all business logic
- API integration tests
- Frontend component tests
- End-to-end user workflow tests
- Performance and accessibility testing
- Quality gates and CI/CD integration

### Phase 6: Security Implementation

#### Step 12: Security Assessment and Implementation
```bash
# Switch to Security Specialist
Security Specialist, I need to conduct a comprehensive security review and implement security measures for the task management SaaS platform.
```

#### Step 13: Execute Security Implementation
```bash
@execute
```

**What happens**: Security Specialist systematically:
- Conducts security audit of all components
- Implements additional security measures
- Sets up vulnerability scanning
- Creates security documentation
- Establishes security monitoring

### Phase 7: Deployment and DevOps

#### Step 14: Setup Production Infrastructure
```bash
# Switch to DevOps Engineer
DevOps Engineer, I need to set up production deployment for the task management SaaS platform with Docker containers, CI/CD pipeline, and monitoring.
```

#### Step 15: Execute Infrastructure Implementation
```bash
@execute
```

**What happens**: DevOps Engineer systematically:
- Creates Docker containers for all services
- Sets up CI/CD pipeline with GitHub Actions
- Configures production environment
- Implements monitoring and logging
- Creates deployment documentation

### Phase 8: Final Quality Review

#### Step 16: Comprehensive Code Review
```bash
# Switch to Test Orchestrator
@code-review "Complete fullstack application review"
```

#### Step 17: Generate Implementation Report
```bash
@execution-report
```

**Final deliverables**:
- Complete fullstack SaaS application
- Production-ready deployment
- Comprehensive documentation
- Quality metrics and performance benchmarks

---

## 🖥️ Walkthrough 2: Cross-Platform TUI Application

**Project**: Developer Productivity CLI Tool  
**Tech Stack**: Rust + Ratatui + SQLite  
**Timeline**: 1-2 weeks  
**Complexity**: Medium

### Phase 1: Project Setup and Architecture

#### Step 1: Initialize TUI Project Planning
```bash
@prime
```

**Your responses** (example):
```
Application Type: Cross-platform Terminal User Interface (TUI) application
Purpose: Developer productivity tool for managing tasks, notes, and time tracking
Target Users: Software developers and technical professionals
Core Features:
- Interactive terminal interface with keyboard navigation
- Task management with categories and priorities
- Note-taking with markdown support
- Time tracking and productivity analytics
- Local SQLite database for data persistence
- Cross-platform support (Windows, macOS, Linux)
Tech Stack: Rust + Ratatui + SQLite
Timeline: 2 weeks for full-featured application
```

#### Step 2: Create TUI-Specific Feature Plan
```bash
@plan-feature "Developer Productivity TUI Tool"
```

**What happens**: Project Manager creates plan optimized for TUI development patterns:
- Terminal interface design and navigation flows
- Keyboard shortcuts and accessibility
- Data persistence and local storage
- Cross-platform compatibility requirements

### Phase 2: Database Design for Local Storage

#### Step 3: Design Local Database Schema
```bash
# Switch to Database Specialist
Database Specialist: I need to design a lightweight SQLite database schema for a TUI productivity application with tasks, notes, time tracking, and user preferences.
```

**What happens**: Database Specialist designs schema optimized for:
- Local SQLite performance
- Simple data relationships
- Fast queries for TUI responsiveness
- Data export/import capabilities

#### Step 4: Execute Database Implementation
```bash
@execute
```

**Expected deliverables**:
- SQLite schema with migration system
- Rust database connection and query modules
- Data models and serialization
- Backup and restore functionality

### Phase 3: Backend Logic and Data Layer

#### Step 5: Implement Core Business Logic
```bash
# Switch to Backend Engineer
Backend Engineer: I need to implement the core business logic for a Rust TUI application with task management, note-taking, and time tracking features using SQLite for local data storage.
```

#### Step 6: Execute Backend Implementation
```bash
@execute
```

**What happens**: Backend Engineer implements:
- Rust application structure with proper modules
- SQLite integration with connection pooling
- Business logic for tasks, notes, and time tracking
- Data validation and error handling
- Configuration management
- Cross-platform file system handling

**Expected deliverables**:
- Core Rust modules in `src/`
- Database abstraction layer
- Business logic implementation
- Configuration and settings management

### Phase 4: TUI Interface Development

#### Step 7: Design Terminal User Interface
```bash
# Switch to Frontend Architect
Frontend Architect: I need to design and implement a terminal user interface using Ratatui for a developer productivity tool. The interface should be intuitive, keyboard-driven, and visually appealing in the terminal.
```

**What happens**: Frontend Architect focuses on:
- Terminal interface design patterns
- Keyboard navigation and shortcuts
- Visual hierarchy in text-based interface
- Responsive terminal layouts

#### Step 8: Execute TUI Implementation
```bash
@execute
```

**What happens**: Frontend Architect builds:
- Ratatui-based terminal interface
- Multiple screens/views (tasks, notes, time tracking)
- Keyboard event handling and navigation
- Terminal-optimized visual design
- Status bars and help systems
- Modal dialogs and forms

**Expected deliverables**:
- Complete TUI interface in `src/ui/`
- Keyboard navigation system
- Multiple application screens
- Terminal-optimized user experience

### Phase 5: Cross-Platform Compatibility

#### Step 9: Ensure Cross-Platform Support
```bash
# Switch to DevOps Engineer
DevOps Engineer: I need to ensure this Rust TUI application works correctly across Windows, macOS, and Linux, with proper build processes and distribution methods.
```

#### Step 10: Execute Cross-Platform Implementation
```bash
@execute
```

**What happens**: DevOps Engineer implements:
- Cross-platform build configuration
- Platform-specific optimizations
- Distribution and packaging
- Installation scripts
- CI/CD for multiple platforms

### Phase 6: Testing and Quality Assurance

#### Step 11: Implement TUI-Specific Testing
```bash
# Switch to Test Orchestrator
Test Orchestrator: I need to implement comprehensive testing for a Rust TUI application, including unit tests, integration tests, and terminal interface testing.
```

#### Step 12: Execute Testing Implementation
```bash
@execute
```

**What happens**: Test Orchestrator creates:
- Unit tests for business logic
- Integration tests for database operations
- TUI interaction testing
- Cross-platform compatibility tests
- Performance benchmarks

### Phase 7: Final Polish and Documentation

#### Step 13: Create User Documentation
```bash
# Switch to UI/UX Designer
UI/UX Designer: I need to create comprehensive user documentation and help systems for the TUI productivity application, focusing on keyboard shortcuts and terminal usage patterns.
```

#### Step 14: Final Quality Review
```bash
@code-review "Cross-platform TUI application review"
```

**Final deliverables**:
- Cross-platform TUI application
- Installation packages for all platforms
- Comprehensive user documentation
- Performance benchmarks

---

## 🤖 Walkthrough 3: Agentic AI Application

**Project**: AI-Powered Code Review Assistant  
**Tech Stack**: Python + FastAPI + LangChain + Vector Database  
**Timeline**: 2-3 weeks  
**Complexity**: High

### Phase 1: AI Application Architecture Planning

#### Step 1: Initialize AI Project Planning
```bash
@prime
```

**Your responses** (example):
```
Application Type: Agentic AI Application - Code Review Assistant
Purpose: AI-powered system that automatically reviews code, suggests improvements, and learns from feedback
Target Users: Development teams and individual developers
Core Features:
- Automated code analysis and review
- AI-powered suggestions and improvements
- Learning from user feedback and corrections
- Integration with Git repositories and CI/CD
- Multi-language code support
- Contextual understanding of codebases
- Collaborative review workflows
Tech Stack: Python + FastAPI + LangChain + ChromaDB + OpenAI API
AI Components: LLM integration, vector embeddings, retrieval-augmented generation
Timeline: 3 weeks for MVP with learning capabilities
```

#### Step 2: Create AI-Specific Architecture Plan
```bash
@plan-feature "AI Code Review Assistant with Learning Capabilities"
```

**What happens**: Project Manager creates plan optimized for AI development:
- AI model integration and prompt engineering
- Vector database for code embeddings
- Learning and feedback loops
- API design for AI services
- Scalability for AI workloads

### Phase 2: AI Infrastructure and Vector Database

#### Step 3: Design AI Data Architecture
```bash
# Switch to Database Specialist
Database Specialist: I need to design a data architecture for an AI code review system that includes vector embeddings for code similarity, user feedback storage, and learning data management.
```

**What happens**: Database Specialist designs:
- Vector database schema for code embeddings
- Relational database for metadata and feedback
- Data pipeline for AI training data
- Performance optimization for vector queries

#### Step 4: Execute AI Database Implementation
```bash
@execute
```

**Expected deliverables**:
- ChromaDB vector database setup
- PostgreSQL for structured data
- Data ingestion pipelines
- Embedding generation workflows

### Phase 3: AI Backend and LLM Integration

#### Step 5: Implement AI Backend Services
```bash
# Switch to Backend Engineer
Backend Engineer: I need to build a FastAPI backend that integrates with LLMs, manages vector embeddings, and provides AI-powered code review capabilities with learning from user feedback.
```

**What happens**: Backend Engineer asks about:
- LLM integration patterns and API usage
- Code analysis and embedding strategies
- Feedback collection and learning mechanisms
- Performance and rate limiting requirements

#### Step 6: Execute AI Backend Implementation
```bash
@execute
```

**What happens**: Backend Engineer implements:
- FastAPI application with async support
- LangChain integration for LLM workflows
- Code parsing and analysis modules
- Vector embedding generation and search
- Feedback collection and learning systems
- AI prompt engineering and optimization

**Expected deliverables**:
- Complete AI backend in `backend/`
- LLM integration with prompt templates
- Code analysis and review engines
- Vector search and similarity matching
- Learning and adaptation mechanisms

### Phase 4: AI Agent Implementation

#### Step 7: Design AI Agent Architecture
```bash
# Switch to Frontend Architect
Frontend Architect: I need to create an intelligent frontend that interfaces with the AI backend, presents code reviews in an intuitive way, and collects user feedback for continuous learning.
```

**What happens**: Frontend Architect focuses on:
- AI-human interaction patterns
- Code review presentation and visualization
- Feedback collection interfaces
- Real-time AI processing indicators

#### Step 8: Execute AI Frontend Implementation
```bash
@execute
```

**What happens**: Frontend Architect builds:
- React application with AI-optimized UX
- Code diff visualization with AI annotations
- Interactive feedback collection
- Real-time AI processing indicators
- Learning progress visualization
- Integration with development tools

**Expected deliverables**:
- AI-powered frontend interface
- Code review visualization
- Feedback collection system
- Developer tool integrations

### Phase 5: AI Model Training and Optimization

#### Step 9: Implement Learning and Adaptation
```bash
# Switch to Backend Engineer (AI focus)
Backend Engineer: I need to implement the learning mechanisms that allow the AI system to improve from user feedback and adapt to different coding styles and preferences.
```

#### Step 10: Execute AI Learning Implementation
```bash
@execute
```

**What happens**: Backend Engineer implements:
- Feedback processing and analysis
- Model fine-tuning workflows
- Prompt optimization based on feedback
- Performance monitoring for AI components
- A/B testing for AI improvements

### Phase 6: AI Security and Ethics

#### Step 11: Implement AI Security Measures
```bash
# Switch to Security Specialist
Security Specialist: I need to implement security measures specific to AI applications, including prompt injection prevention, data privacy for code analysis, and secure API usage.
```

#### Step 12: Execute AI Security Implementation
```bash
@execute
```

**What happens**: Security Specialist implements:
- Prompt injection prevention
- Code privacy and data protection
- API rate limiting and abuse prevention
- AI model security measures
- Audit logging for AI decisions

### Phase 7: AI Testing and Validation

#### Step 13: Implement AI-Specific Testing
```bash
# Switch to Test Orchestrator
Test Orchestrator: I need to implement comprehensive testing for an AI application, including AI model validation, prompt testing, and learning system verification.
```

#### Step 14: Execute AI Testing Implementation
```bash
@execute
```

**What happens**: Test Orchestrator creates:
- AI model accuracy testing
- Prompt engineering validation
- Learning system verification
- Performance benchmarks for AI operations
- User acceptance testing for AI features

### Phase 8: AI Deployment and Monitoring

#### Step 15: Setup AI Production Infrastructure
```bash
# Switch to DevOps Engineer
DevOps Engineer: I need to set up production infrastructure for an AI application with GPU support, model serving, vector database hosting, and AI-specific monitoring.
```

#### Step 16: Execute AI Infrastructure Implementation
```bash
@execute
```

**What happens**: DevOps Engineer implements:
- GPU-enabled container deployment
- Vector database hosting and scaling
- AI model serving infrastructure
- Performance monitoring for AI workloads
- Cost optimization for AI API usage

### Phase 9: AI Quality and Ethics Review

#### Step 17: Comprehensive AI System Review
```bash
@code-review "AI application with ethical considerations"
```

#### Step 18: Generate AI Implementation Report
```bash
@execution-report
```

**Final deliverables**:
- Complete AI-powered code review system
- Learning and adaptation capabilities
- Production AI infrastructure
- Comprehensive AI testing and validation
- Ethics and security documentation

---

## 🎯 Key Success Patterns

### Universal Workflow Pattern
1. **@prime** - Always start with comprehensive project context loading
2. **@plan-feature** - Create detailed implementation plans
3. **@execute** - Use systematic implementation for each agent
4. **@code-review** - Ensure quality at major milestones
5. **@execution-report** - Document and analyze results

### Agent Coordination Pattern
1. **Project Manager** - Overall coordination and planning
2. **Database Specialist** - Data architecture and persistence
3. **Backend Engineer** - Core business logic and APIs
4. **Frontend Architect** - User interface and experience
5. **Test Orchestrator** - Quality assurance and testing
6. **Security Specialist** - Security and compliance
7. **DevOps Engineer** - Infrastructure and deployment
8. **UI/UX Designer** - User experience optimization
9. **Development Logger** - Process improvement and learning

### Quality Gates
1. **Planning Gate** - Comprehensive requirements and architecture
2. **Implementation Gate** - Systematic development with @execute
3. **Quality Gate** - Code review and testing validation
4. **Security Gate** - Security assessment and compliance
5. **Deployment Gate** - Production readiness and monitoring

## 📚 Next Steps

After completing any walkthrough:

1. **Review the implementation** with `@code-review`
2. **Generate comprehensive report** with `@execution-report`
3. **Analyze process effectiveness** with Development Logger
4. **Plan next iteration** based on learnings and feedback
5. **Update documentation** and share insights with team

Each walkthrough demonstrates the power of systematic development with the Kiro-CLI Agent Team System, ensuring consistent quality and comprehensive coverage regardless of project type or complexity.