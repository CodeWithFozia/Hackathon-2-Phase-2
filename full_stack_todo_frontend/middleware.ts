// T022: Middleware for route protection

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Note: Middleware cannot access localStorage, so we rely on client-side AuthContext
  // for actual authentication checks. This middleware just handles basic routing.

  // Allow all requests to pass through
  // AuthContext will handle redirects based on localStorage token
  return NextResponse.next();
}

export const config = {
  matcher: ['/tasks/:path*', '/signin', '/signup'],
};
