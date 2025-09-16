# Cursor AI Instructions for Nanny Match Project

## 🎯 PROJECT CONTEXT

This is a **WORKING PRODUCTION-READY** nanny matching platform with:
- **Backend**: FastAPI + PostgreSQL + Redis (all via Docker)
- **Frontend**: React + Vite + TypeScript (local development)
- **Architecture**: Microservices with Docker containers

## 🚨 CRITICAL CONSTRAINTS

### NEVER DO WITHOUT EXPLICIT USER REQUEST:
- Rewrite working scripts (`restart-all.sh`, `start-both.sh`)
- Change Docker configurations that work
- Modify database connections or Redis setup
- Switch services from Docker to local or vice versa
- Delete any `.md`, `.sh`, or config files
- "Refactor" working code

### ALWAYS DO:
- Test changes immediately with `./restart-all.sh`
- Make minimal changes only
- Ask user before architectural changes
- Document what and why you changed
- Keep existing patterns and structures

## 🔧 DEVELOPMENT WORKFLOW

### 1. Understanding Current State:
```bash
# Check what's running
docker ps
curl -s http://localhost:8000/health  # Backend
curl -s http://localhost:8080         # Frontend
```

### 2. Making Changes:
- **Read existing code** first to understand patterns
- **Use existing structures** - don't reinvent
- **Add features** without breaking existing ones
- **Test immediately** after each change

### 3. Verification:
```bash
# Must pass after every change
./restart-all.sh
# All services should start successfully
```

## 📁 PROJECT STRUCTURE

### Key Directories:
- `nanny-match-backend/` - FastAPI backend (Docker)
- `nanny-match-ukraine/` - React frontend (local)
- `.cursor/` - AI instructions (this folder)

### Important Files:
- `restart-all.sh` - Main startup script (CRITICAL - DON'T MODIFY)
- `CURSOR_WORKSPACE.md` - Detailed project documentation
- `docker-compose.dev.yml` - Backend Docker configuration
- `package.json` - Frontend dependencies

### Configuration:
- Backend uses Docker containers for all services
- Frontend runs locally with npm/vite
- Database: PostgreSQL via Docker
- Cache: Redis via Docker

## 🎨 CODING STANDARDS

### Backend (FastAPI):
- Follow existing patterns in `app/main.py`
- Use Pydantic models for validation
- Maintain Docker compatibility
- Keep database migrations in alembic

### Frontend (React):
- Use TypeScript strictly
- Follow existing component patterns
- Maintain Tailwind CSS classes
- Use existing hooks and contexts

## 🔍 COMMON TASKS

### Adding New API Endpoint:
1. Add route to `app/main.py` or appropriate router
2. Create Pydantic models if needed
3. Test with existing Docker setup
4. Update frontend adapter if needed

### Adding New UI Component:
1. Create in `src/components/`
2. Follow existing patterns
3. Use TypeScript interfaces
4. Test with local development server

### Database Changes:
1. Create Alembic migration
2. Test with Docker PostgreSQL
3. Update models accordingly
4. Don't break existing data

## 🚨 ERROR HANDLING

### If Build Fails:
1. Check Docker containers are running
2. Verify environment variables
3. Check for missing dependencies
4. Revert to last working state

### If Tests Fail:
1. Run `./restart-all.sh` first
2. Check backend health endpoint
3. Verify frontend loads
4. Check Docker container logs

## 📋 CHANGE CHECKLIST

Before completing any task:
- [ ] Code follows existing patterns
- [ ] No working functionality is broken
- [ ] `./restart-all.sh` works successfully
- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] Docker containers are healthy
- [ ] Changes are minimal and focused
- [ ] User requirements are met exactly

## 🎯 SUCCESS DEFINITION

A task is complete ONLY when:
1. **Functionality works** as requested
2. **Existing features** remain unbroken  
3. **All services start** via `./restart-all.sh`
4. **No new errors** are introduced
5. **User can verify** the changes work

## 💬 COMMUNICATION

### When Reporting Progress:
- Show what was changed specifically
- Explain why the change was needed
- Provide verification steps
- Mention any potential impacts

### When Asking for Clarification:
- Reference existing working code
- Suggest minimal change approaches
- Ask about specific implementation details
- Confirm architectural preferences

## 🔄 REMEMBER

This is a **WORKING SYSTEM**. The user prefers:
- **Stability** over perfection
- **Minimal changes** over comprehensive refactoring  
- **Proven patterns** over new approaches
- **Working code** over theoretical improvements

**Your job is to help, not to "fix" what already works.**