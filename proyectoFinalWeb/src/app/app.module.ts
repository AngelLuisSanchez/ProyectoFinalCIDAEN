import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
// Rutas
import { APP_ROUTING } from './app.routes';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { CloudtagComponent } from './components/cloudtag/cloudtag.component';

import { TagCloudModule } from 'angular-tag-cloud-module';

@NgModule({
  declarations: [AppComponent, HomeComponent, NavbarComponent, CloudtagComponent],
  imports: [BrowserModule, HttpModule, APP_ROUTING, TagCloudModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
