<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1400px; margin: 0 auto;">
      <!-- Header -->
      <div class="row items-center q-mb-lg">
        <div class="col">
          <h2 class="text-h3 q-my-none">Analytics Dashboard</h2>
          <p class="text-subtitle1 text-grey-7" v-if="organization">
            {{ organization.name }}
          </p>
        </div>
        <div class="col-auto">
          <q-btn-group unelevated>
            <q-btn color="primary" label="Export PDF" icon="picture_as_pdf" @click="exportPDF" />
            <q-btn color="primary" label="Export CSV" icon="table_chart" @click="exportCSV" />
          </q-btn-group>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
      </div>

      <!-- Dashboard Content -->
      <div v-else-if="organization">
        <!-- Key Metrics -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="metric-card">
              <q-card-section>
                <div class="metric-icon bg-primary">
                  <q-icon name="people" size="md" color="white" />
                </div>
                <div class="metric-value">{{ stats.total_participants }}</div>
                <div class="metric-label">Total Members</div>
                <div class="metric-change text-positive">
                  <q-icon name="trending_up" size="xs" />
                  +{{ stats.new_members_this_month }} this month
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="metric-card">
              <q-card-section>
                <div class="metric-icon bg-green">
                  <q-icon name="check_circle" size="md" color="white" />
                </div>
                <div class="metric-value">{{ stats.total_pledges }}</div>
                <div class="metric-label">Total Pledges</div>
                <div class="metric-change text-positive">
                  {{ stats.active_pledges }} active
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="metric-card">
              <q-card-section>
                <div class="metric-icon bg-blue">
                  <q-icon name="eco" size="md" color="white" />
                </div>
                <div class="metric-value">{{ stats.total_carbon_saved_kg.toFixed(0) }}</div>
                <div class="metric-label">kg CO₂ Saved</div>
                <div class="metric-change text-positive">
                  {{ (stats.total_carbon_saved_kg / stats.total_participants).toFixed(1) }} per member
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="metric-card">
              <q-card-section>
                <div class="metric-icon bg-amber">
                  <q-icon name="emoji_events" size="md" color="white" />
                </div>
                <div class="metric-value">{{ completionRate }}%</div>
                <div class="metric-label">Completion Rate</div>
                <div class="metric-change text-positive">
                  {{ stats.completed_pledges }} completed
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="row q-col-gutter-md q-mb-lg">
          <!-- Pledge Activity Chart -->
          <div class="col-12 col-md-8">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">Pledge Activity Over Time</div>
                <div class="chart-placeholder">
                  <q-icon name="show_chart" size="64px" color="grey-5" />
                  <div class="text-grey-7 q-mt-sm">Chart visualization (requires Chart.js integration)</div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Category Breakdown -->
          <div class="col-12 col-md-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">Pledge Categories</div>
                <div class="category-list">
                  <div v-for="category in categoryBreakdown" :key="category.name" class="category-item">
                    <div class="row items-center q-gutter-sm">
                      <q-icon :name="category.icon" :color="category.color" size="sm" />
                      <div class="col">
                        <div class="text-body2">{{ category.name }}</div>
                        <q-linear-progress
                          :value="category.percentage / 100"
                          :color="category.color"
                          size="8px"
                          class="q-mt-xs"
                        />
                      </div>
                      <div class="text-caption text-weight-bold">{{ category.count }}</div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Impact Breakdown -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <div class="text-h6 q-mb-md">Environmental Impact Breakdown</div>
          </div>
          <div class="col-12 col-sm-6 col-lg-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="eco" size="48px" color="green" />
                <div class="text-h5 text-green q-mt-sm">{{ stats.total_carbon_saved_kg.toFixed(1) }} kg</div>
                <div class="text-caption text-grey-7">Carbon Dioxide Saved</div>
                <q-separator class="q-my-md" />
                <div class="text-caption">
                  Equivalent to {{ (stats.total_carbon_saved_kg / 0.404).toFixed(0) }} km not driven
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-lg-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="water_drop" size="48px" color="blue" />
                <div class="text-h5 text-blue q-mt-sm">{{ stats.total_water_saved_liters.toFixed(0) }} L</div>
                <div class="text-caption text-grey-7">Water Conserved</div>
                <q-separator class="q-my-md" />
                <div class="text-caption">
                  Equivalent to {{ (stats.total_water_saved_liters / 50).toFixed(0) }} showers saved
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-lg-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="recycling" size="48px" color="teal" />
                <div class="text-h5 text-teal q-mt-sm">{{ stats.total_plastic_saved_kg.toFixed(1) }} kg</div>
                <div class="text-caption text-grey-7">Plastic Prevented</div>
                <q-separator class="q-my-md" />
                <div class="text-caption">
                  Equivalent to {{ (stats.total_plastic_saved_kg / 0.014).toFixed(0) }} bottles avoided
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-lg-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="park" size="48px" color="green-7" />
                <div class="text-h5 text-green q-mt-sm">{{ stats.total_trees_equivalent.toFixed(1) }}</div>
                <div class="text-caption text-grey-7">Tree Equivalents</div>
                <q-separator class="q-my-md" />
                <div class="text-caption">
                  Trees planted equivalent
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Top Members -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">Top Contributors</div>
                <q-list separator>
                  <q-item v-for="(member, index) in topMembers" :key="member.id">
                    <q-item-section avatar>
                      <q-avatar :color="index < 3 ? 'amber' : 'grey-5'" text-color="white">
                        {{ index + 1 }}
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ member.name }}</q-item-label>
                      <q-item-label caption>{{ member.email }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-chip dense color="primary" text-color="white">
                        {{ member.pledge_count }} pledges
                      </q-chip>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </q-card>
          </div>

          <!-- Recent Activity -->
          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">Recent Activity</div>
                <q-list separator>
                  <q-item v-for="activity in recentActivity" :key="activity.id">
                    <q-item-section avatar>
                      <q-avatar :color="getActivityColor(activity.activity_type)" text-color="white">
                        <q-icon :name="getActivityIcon(activity.activity_type)" />
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ activity.user.name }}</q-item-label>
                      <q-item-label caption>{{ activity.activity_text }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-item-label caption>{{ formatTimeAgo(activity.created_at) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Organization Settings -->
        <div class="row q-col-gutter-md">
          <div class="col-12">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">Organization Settings</div>
                <div class="row q-col-gutter-md">
                  <div class="col-12 col-sm-6">
                    <q-input v-model="organization.access_code" label="Access Code" outlined readonly>
                      <template v-slot:append>
                        <q-btn flat dense icon="content_copy" @click="copyAccessCode" />
                      </template>
                    </q-input>
                  </div>
                  <div class="col-12 col-sm-6">
                    <q-input v-model="organization.simple_url" label="Simple URL" outlined readonly>
                      <template v-slot:append>
                        <q-btn flat dense icon="content_copy" @click="copyURL" />
                      </template>
                    </q-input>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useRoute } from 'vue-router'

export default defineComponent({
  name: 'AnalyticsPage',

  setup() {
    const $q = useQuasar()
    const route = useRoute()
    const loading = ref(true)
    const organization = ref(null)
    const stats = ref({})
    const topMembers = ref([])
    const recentActivity = ref([])

    const orgId = ref(route.params.orgId || 1)

    const completionRate = computed(() => {
      if (!stats.value.total_pledges) return 0
      return Math.round((stats.value.completed_pledges / stats.value.total_pledges) * 100)
    })

    const categoryBreakdown = computed(() => {
      // Mock data - would be calculated from actual pledge data
      return [
        { name: 'Carbon Reduction', icon: 'eco', color: 'green', count: 45, percentage: 35 },
        { name: 'Water Conservation', icon: 'water_drop', color: 'blue', count: 30, percentage: 23 },
        { name: 'Plastic Reduction', icon: 'recycling', color: 'teal', count: 25, percentage: 19 },
        { name: 'Waste Reduction', icon: 'delete', color: 'orange', count: 20, percentage: 15 },
        { name: 'Energy Conservation', icon: 'bolt', color: 'amber', count: 10, percentage: 8 }
      ]
    })

    const loadAnalytics = async () => {
      loading.value = true
      try {
        // Load organization
        const orgResponse = await api.get(`/api/organizations/${orgId.value}`)
        organization.value = orgResponse.data

        // Load impact stats
        const statsResponse = await api.get(`/api/impact/organization/${orgId.value}`)
        stats.value = statsResponse.data
        stats.value.new_members_this_month = Math.floor(stats.value.total_participants * 0.15) // Mock

        // Load recent activity
        const activityResponse = await api.get('/api/activity/', {
          params: { organization_id: orgId.value, limit: 5 }
        })
        recentActivity.value = activityResponse.data

        // Mock top members data
        topMembers.value = [
          { id: 1, name: 'John Doe', email: 'john@example.com', pledge_count: 12 },
          { id: 2, name: 'Jane Smith', email: 'jane@example.com', pledge_count: 10 },
          { id: 3, name: 'Bob Johnson', email: 'bob@example.com', pledge_count: 8 },
          { id: 4, name: 'Alice Williams', email: 'alice@example.com', pledge_count: 7 },
          { id: 5, name: 'Charlie Brown', email: 'charlie@example.com', pledge_count: 6 }
        ]
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load analytics'
        })
      } finally {
        loading.value = false
      }
    }

    const exportPDF = () => {
      $q.notify({
        type: 'info',
        message: 'PDF export would generate a comprehensive report with all analytics',
        timeout: 3000
      })
      // Would integrate with a PDF library like jsPDF
    }

    const exportCSV = () => {
      if (!stats.value) return

      // Generate CSV data
      const csvData = [
        ['Metric', 'Value'],
        ['Organization', organization.value.name],
        ['Total Members', stats.value.total_participants],
        ['Total Pledges', stats.value.total_pledges],
        ['Active Pledges', stats.value.active_pledges],
        ['Completed Pledges', stats.value.completed_pledges],
        ['Carbon Saved (kg)', stats.value.total_carbon_saved_kg.toFixed(2)],
        ['Water Saved (L)', stats.value.total_water_saved_liters.toFixed(2)],
        ['Plastic Prevented (kg)', stats.value.total_plastic_saved_kg.toFixed(2)],
        ['Trees Equivalent', stats.value.total_trees_equivalent.toFixed(2)],
        ['Completion Rate', `${completionRate.value}%`]
      ]

      const csv = csvData.map(row => row.join(',')).join('\n')
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${organization.value.name}-analytics.csv`
      a.click()
      window.URL.revokeObjectURL(url)

      $q.notify({
        type: 'positive',
        message: 'CSV exported successfully!'
      })
    }

    const copyAccessCode = () => {
      navigator.clipboard.writeText(organization.value.access_code)
      $q.notify({
        type: 'positive',
        message: 'Access code copied!',
        timeout: 1000
      })
    }

    const copyURL = () => {
      navigator.clipboard.writeText(`/join/${organization.value.simple_url}`)
      $q.notify({
        type: 'positive',
        message: 'URL copied!',
        timeout: 1000
      })
    }

    const getActivityIcon = (type) => {
      const icons = {
        pledge_created: 'add_task',
        pledge_completed: 'check_circle',
        badge_earned: 'emoji_events',
        milestone_reached: 'celebration'
      }
      return icons[type] || 'notifications'
    }

    const getActivityColor = (type) => {
      const colors = {
        pledge_created: 'blue',
        pledge_completed: 'green',
        badge_earned: 'amber',
        milestone_reached: 'purple'
      }
      return colors[type] || 'grey'
    }

    const formatTimeAgo = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)

      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      if (diffHours < 24) return `${diffHours}h ago`
      return `${diffDays}d ago`
    }

    onMounted(() => {
      loadAnalytics()
    })

    return {
      loading,
      organization,
      stats,
      topMembers,
      recentActivity,
      completionRate,
      categoryBreakdown,
      exportPDF,
      exportCSV,
      copyAccessCode,
      copyURL,
      getActivityIcon,
      getActivityColor,
      formatTimeAgo
    }
  }
})
</script>

<style scoped>
.metric-card {
  transition: transform 0.2s;
}

.metric-card:hover {
  transform: translateY(-4px);
}

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.metric-value {
  font-size: 2rem;
  font-weight: bold;
  line-height: 1;
}

.metric-label {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

.metric-change {
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-item {
  padding: 0.5rem 0;
}
</style>
