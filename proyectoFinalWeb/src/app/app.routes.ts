import { RouterModule, Routes, Router } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CloudtagComponent } from './components/cloudtag/cloudtag.component';

const APP_ROUTES: Routes = [
    { path: 'home', component: HomeComponent },
    { path: 'cloudtag', component: CloudtagComponent },
    { path: '**', pathMatch: 'full', redirectTo: 'home' }
];

export const APP_ROUTING = RouterModule.forRoot(APP_ROUTES, { useHash: true });
