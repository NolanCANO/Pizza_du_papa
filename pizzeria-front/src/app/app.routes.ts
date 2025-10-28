import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/menu',
    pathMatch: 'full'
  },
  {
    path: 'menu',
    loadComponent: () => import('./features/menu/menu.page').then(m => m.MenuPage)
  },
  {
    path: 'cart',
    loadComponent: () => import('./features/cart/cart.page').then(m => m.CartPage)
  },
  {
    path: 'checkout',
    loadComponent: () => import('./features/checkout/checkout.page').then(m => m.CheckoutPage)
  },
  {
    path: 'orders/:id',
    loadComponent: () => import('./features/order-tracking/order-tracking.page').then(m => m.OrderTrackingPage)
  },
  {
    path: 'stocks',
    loadComponent: () => import('./features/stocks/stocks.page').then(m => m.StocksPage)
  }
];
