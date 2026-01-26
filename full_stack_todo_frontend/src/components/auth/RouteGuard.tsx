'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/lib/hooks/useAuth';

export function RouteGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    // Don't redirect while checking auth status
    if (loading) return;

    const isProtectedRoute = pathname?.startsWith('/tasks');
    const isAuthRoute = pathname === '/signin' || pathname === '/signup';

    // Redirect to signin if trying to access protected route without auth
    if (isProtectedRoute && !isAuthenticated) {
      router.push('/signin');
    }

    // Redirect to tasks if already authenticated and on auth pages
    if (isAuthRoute && isAuthenticated) {
      router.push('/tasks');
    }
  }, [isAuthenticated, loading, pathname, router]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-dark">
        <div className="flex flex-col items-center gap-3">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-500"></div>
          <p className="text-gray-400 text-sm">Loading...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
