<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          <div class="row items-center no-wrap">
            <q-icon name="eco" size="sm" class="q-mr-sm" />
            <span class="text-weight-bold">Planet Pledge</span>
          </div>
        </q-toolbar-title>

        <q-btn flat label="Home" to="/" />
        <q-btn flat label="Make a Pledge" to="/pledge" />
        <q-btn flat label="Impact" to="/impact" />
        <q-btn flat label="Community" to="/community" />
        <q-btn flat label="Stories" to="/stories" />

        <q-space />

        <q-btn flat round dense icon="more_vert">
          <q-menu>
            <q-list style="min-width: 180px">
              <q-item clickable v-close-popup to="/dashboard">
                <q-item-section avatar>
                  <q-icon name="dashboard" />
                </q-item-section>
                <q-item-section>My Dashboard</q-item-section>
              </q-item>
              <q-item clickable v-close-popup to="/profile/1">
                <q-item-section avatar>
                  <q-icon name="person" />
                </q-item-section>
                <q-item-section>My Profile</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup to="/my-pledges">
                <q-item-section avatar>
                  <q-icon name="check_circle" />
                </q-item-section>
                <q-item-section>My Pledges</q-item-section>
              </q-item>
              <q-item clickable v-close-popup to="/campaigns">
                <q-item-section avatar>
                  <q-icon name="campaign" />
                </q-item-section>
                <q-item-section>Campaigns</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup to="/organize">
                <q-item-section avatar>
                  <q-icon name="groups" />
                </q-item-section>
                <q-item-section>Organize</q-item-section>
              </q-item>
              <q-item clickable v-close-popup to="/cms">
                <q-item-section avatar>
                  <q-icon name="settings" />
                </q-item-section>
                <q-item-section>CMS</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title class="text-center">
          <div class="text-caption">
            Together we can make a difference for our planet
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainLayout'
})
</script>
