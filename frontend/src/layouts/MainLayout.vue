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
        <q-btn flat label="Campaigns" to="/campaigns" />
        <q-btn flat label="Organize" to="/organize" />

        <q-space />

        <q-btn flat round dense icon="more_vert">
          <q-menu>
            <q-list style="min-width: 150px">
              <q-item clickable v-close-popup to="/my-pledges">
                <q-item-section avatar>
                  <q-icon name="check_circle" />
                </q-item-section>
                <q-item-section>My Pledges</q-item-section>
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
