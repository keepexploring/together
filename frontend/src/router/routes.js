const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'pledge', name: 'pledge', component: () => import('pages/PledgePage.vue') },
      { path: 'join/:code', name: 'join', component: () => import('pages/JoinPage.vue') },
      { path: 'impact', name: 'impact', component: () => import('pages/ImpactPage.vue') },
      { path: 'campaigns', name: 'campaigns', component: () => import('pages/CampaignsPage.vue') },
      { path: 'campaign/:id', name: 'campaign-detail', component: () => import('pages/CampaignDetailPage.vue') },
      { path: 'organize', name: 'organize', component: () => import('pages/OrganizePage.vue') },
      { path: 'my-pledges', name: 'my-pledges', component: () => import('pages/MyPledgesPage.vue') },
      { path: 'cms', name: 'cms', component: () => import('pages/CMSPage.vue') },
      { path: 'profile/:userId?', name: 'profile', component: () => import('pages/ProfilePage.vue') },
      { path: 'dashboard', name: 'dashboard', component: () => import('pages/DashboardPage.vue') },
      { path: 'community', name: 'community', component: () => import('pages/CommunityFeedPage.vue') },
      { path: 'stories', name: 'stories', component: () => import('pages/StoriesPage.vue') }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
