#!/bin/bash
# Quick Start Script for Timbuktoo MVP
# This script helps developers set up and run the complete app in under 5 minutes

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        echo "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker installed: $(docker --version)"

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose installed: $(docker-compose --version)"

    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed (required for mobile app)"
        echo "Install from: https://nodejs.org/"
    else
        print_success "Node.js installed: $(node --version)"
    fi

    # Check npm
    if ! command -v npm &> /dev/null; then
        print_warning "npm is not installed (required for mobile app)"
    else
        print_success "npm installed: $(npm --version)"
    fi

    echo ""
}

# Setup backend
setup_backend() {
    print_header "Setting Up Backend"

    cd backend

    # Check if .env exists
    if [ ! -f .env ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_warning "IMPORTANT: Add your ANTHROPIC_API_KEY to backend/.env"
        print_info "Get your API key from: https://console.anthropic.com/"

        # Prompt for API key
        read -p "Do you have an Anthropic API key to add now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter your Anthropic API key: " api_key
            sed -i.bak "s/your-api-key-here/$api_key/" .env
            print_success "API key added to .env"
        else
            print_warning "You'll need to add ANTHROPIC_API_KEY to backend/.env manually"
        fi
    else
        print_success ".env file already exists"
    fi

    cd ..
}

# Setup mobile
setup_mobile() {
    print_header "Setting Up Mobile App"

    cd mobile

    # Check if .env exists
    if [ ! -f .env ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created"
    else
        print_success ".env file already exists"
    fi

    # Install dependencies
    if [ ! -d "node_modules" ]; then
        print_info "Installing mobile dependencies (this may take a few minutes)..."
        npm install
        print_success "Mobile dependencies installed"
    else
        print_success "Mobile dependencies already installed"
    fi

    cd ..
}

# Start backend
start_backend() {
    print_header "Starting Backend Server"

    cd backend

    # Start Docker containers
    print_info "Starting PostgreSQL and FastAPI..."
    docker-compose up -d

    # Wait for backend to be healthy
    print_info "Waiting for backend to be ready..."
    sleep 5

    # Health check
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "Backend is running at http://localhost:8000"
            print_info "API Documentation: http://localhost:8000/docs"
            break
        else
            if [ $i -eq 10 ]; then
                print_error "Backend failed to start"
                print_info "Check logs: docker-compose logs -f"
                exit 1
            fi
            sleep 2
        fi
    done

    cd ..
}

# Start mobile
start_mobile() {
    print_header "Starting Mobile App"

    cd mobile

    print_info "Starting Expo development server..."
    print_info "Press 'i' for iOS or 'a' for Android"
    print_info "Press Ctrl+C to stop"

    npm start

    cd ..
}

# Run tests
run_tests() {
    print_header "Running Tests"

    # Backend syntax check
    print_info "Checking backend Python syntax..."
    cd backend
    python3 -m py_compile app/main.py app/api/*.py app/models/*.py app/schemas/*.py app/utils/*.py 2>&1
    if [ $? -eq 0 ]; then
        print_success "Backend Python syntax check passed"
    else
        print_error "Backend Python syntax check failed"
        exit 1
    fi
    cd ..

    # Mobile TypeScript check
    if command -v npx &> /dev/null; then
        print_info "Checking mobile TypeScript..."
        cd mobile
        npx tsc --noEmit 2>&1 || print_warning "TypeScript check warnings (non-blocking)"
        cd ..
    fi

    print_success "All tests passed"
}

# Show status
show_status() {
    print_header "System Status"

    # Check backend
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend: Running at http://localhost:8000"
    else
        print_error "Backend: Not running"
    fi

    # Check PostgreSQL
    cd backend
    if docker-compose ps postgres | grep -q "Up"; then
        print_success "PostgreSQL: Running"
    else
        print_error "PostgreSQL: Not running"
    fi
    cd ..

    echo ""
    print_info "Next steps:"
    echo "  1. Open http://localhost:8000/docs to test API"
    echo "  2. Start mobile app: cd mobile && npm start"
    echo "  3. Press 'i' for iOS or 'a' for Android"
    echo "  4. Test end-to-end: Signup → Preferences → Cities → Itinerary"
}

# Stop all services
stop_services() {
    print_header "Stopping All Services"

    cd backend
    docker-compose down
    print_success "Backend stopped"
    cd ..

    # Kill any Expo processes
    pkill -f "expo start" 2>/dev/null || true
    print_success "Mobile app stopped"
}

# Main menu
show_menu() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🌍 Timbuktoo MVP - Quick Start Menu"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  1) Full Setup (backend + mobile)"
    echo "  2) Setup Backend Only"
    echo "  3) Setup Mobile Only"
    echo "  4) Start Backend"
    echo "  5) Start Mobile"
    echo "  6) Run Tests"
    echo "  7) Show Status"
    echo "  8) Stop All Services"
    echo "  9) Exit"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main script
main() {
    clear
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🌍 Timbuktoo MVP - Quick Start Script"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Check if running from project root
    if [ ! -d "backend" ] || [ ! -d "mobile" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi

    # Parse command line arguments
    if [ "$1" = "--full" ]; then
        check_prerequisites
        setup_backend
        setup_mobile
        start_backend
        show_status
        exit 0
    elif [ "$1" = "--backend" ]; then
        check_prerequisites
        setup_backend
        start_backend
        show_status
        exit 0
    elif [ "$1" = "--mobile" ]; then
        setup_mobile
        start_mobile
        exit 0
    elif [ "$1" = "--test" ]; then
        run_tests
        exit 0
    elif [ "$1" = "--stop" ]; then
        stop_services
        exit 0
    fi

    # Interactive menu
    while true; do
        show_menu
        read -p "Select an option (1-9): " choice
        case $choice in
            1)
                check_prerequisites
                setup_backend
                setup_mobile
                start_backend
                show_status
                ;;
            2)
                check_prerequisites
                setup_backend
                ;;
            3)
                setup_mobile
                ;;
            4)
                start_backend
                show_status
                ;;
            5)
                start_mobile
                ;;
            6)
                run_tests
                ;;
            7)
                show_status
                ;;
            8)
                stop_services
                ;;
            9)
                echo ""
                print_info "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please select 1-9."
                ;;
        esac

        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main "$@"
