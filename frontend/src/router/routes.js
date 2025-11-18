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
      { path: 'cms', name: 'cms', component: () => import('pages/CMSPage.vue') }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
