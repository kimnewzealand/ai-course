# Admin UI

A modern web interface for managing items through the REST API, built with vanilla TypeScript, HTML, and CSS.

## Features

- ✅ **Item Management**: Create, read, update, and delete items
- ✅ **Real-time Validation**: Client-side form validation with user feedback
- ✅ **Responsive Design**: Works on desktop and mobile devices
- ✅ **API Integration**: Connects to the FastAPI backend using fetch
- ✅ **Modern UI**: Clean, accessible interface with smooth interactions
- ✅ **TypeScript**: Full type safety and modern JavaScript features

## Setup

1. Ensure the API server is running on `http://localhost:8000`
2. Install pnpm: `npm install -g pnpm`
3. Install dependencies: `pnpm install`
4. Start development server: `pnpm dev`

The admin interface will be available at `http://localhost:3000`

## Development

### Available Scripts

- `pnpm dev` - Start development server with hot reload
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build
- `pnpm test` - Run unit tests
- `pnpm test:e2e` - Run end-to-end tests
- `pnpm lint` - Run ESLint
- `pnpm format` - Format code with Prettier

### Project Structure

```
src/
├── components/
│   └── ApiService.ts      # API communication
├── types/
│   └── index.ts           # TypeScript interfaces
├── utils/
│   └── validation.ts      # Form validation logic
├── styles/
│   └── main.css           # Application styles
└── main.ts                # Application entry point
```

## API Integration

The interface connects to the REST API at `http://localhost:8000` with the following endpoints:

- `GET /v1/items` - List all items
- `POST /v1/items` - Create new item
- `GET /v1/items/{id}` - Get specific item
- `PUT /v1/items/{id}` - Update item
- `DELETE /v1/items/{id}` - Delete item

## Validation Rules

- **Name**: Required, 1-100 characters
- **Description**: Optional, maximum 500 characters

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Uses modern web APIs including:
- Fetch API for HTTP requests
- ES6 Modules
- CSS Grid and Flexbox
- CSS Custom Properties

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Ensure TypeScript types are properly defined
4. Test across different browsers
