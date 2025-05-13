import uvicorn
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run BBQ Nation Chatbot API')
    parser.add_argument('--host', default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    
    args = parser.parse_args()
    
    print(f"Starting BBQ Nation Chatbot API on {args.host}:{args.port}")
    print("Documentation available at:")
    print(f"- Swagger UI: http://{args.host}:{args.port}/docs")
    print(f"- ReDoc: http://{args.host}:{args.port}/redoc")
    
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main() 