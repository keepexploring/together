<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1400px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">My Dashboard</h2>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
      </div>

      <!-- Dashboard Content -->
      <div v-else-if="profile">
        <!-- Quick Stats Row -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="stat-card">
              <q-card-section>
                <div class="stat-value text-primary">{{ profile.total_pledges }}</div>
                <div class="stat-label">Total Pledges</div>
                <div class="stat-trend text-positive">
                  <q-icon name="trending_up" /> {{ profile.active_pledges }} active
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="stat-card">
              <q-card-section>
                <div class="stat-value text-green">{{ profile.badges_earned.length }}</div>
                <div class="stat-label">Badges Earned</div>
                <div class="stat-trend text-grey-7">
                  <q-icon name="emoji_events" /> Keep going!
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="stat-card">
              <q-card-section>
                <div class="stat-value text-orange">{{ profile.current_streak_days }}</div>
                <div class="stat-label">Day Streak</div>
                <div class="stat-trend text-grey-7">
                  <q-icon name="local_fire_department" /> Daily goal
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="stat-card">
              <q-card-section>
                <div class="stat-value text-purple">{{ profile.completed_pledges }}</div>
                <div class="stat-label">Completed</div>
                <div class="stat-trend text-positive">
                  {{ completionRate.toFixed(0) }}% success
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Environmental Impact Charts -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Environmental Impact</div>
          </div>

          <!-- Carbon Impact -->
          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="eco" color="green-7" size="sm" />
                  Carbon Saved
                </div>
                <div class="impact-display">
                  <div class="impact-value">{{ profile.total_carbon_saved.toFixed(1) }}</div>
                  <div class="impact-unit">kg CO₂</div>
                </div>
                <div class="impact-comparison q-mt-md">
                  <div class="text-caption text-grey-7">Equivalent to:</div>
                  <div class="comparison-items">
                    <div class="comparison-item">
                      <q-icon name="directions_car" color="grey-7" />
                      {{ (profile.total_carbon_saved / 0.404).toFixed(0) }} km driven
                    </div>
                    <div class="comparison-item">
                      <q-icon name="park" color="green-7" />
                      {{ (profile.total_carbon_saved / 21.77).toFixed(1) }} trees planted
                    </div>
                  </div>
                </div>
                <!-- Visual Bar -->
                <div class="q-mt-md">
                  <div class="progress-bar-container">
                    <div
                      class="progress-bar-fill bg-green"
                      :style="{ width: Math.min((profile.total_carbon_saved / 1000) * 100, 100) + '%' }"
                    ></div>
                  </div>
                  <div class="text-caption text-grey-7 q-mt-xs">
                    {{ (profile.total_carbon_saved / 1000 * 100).toFixed(0) }}% to 1 ton goal
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Water & Plastic Impact -->
          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">
                  <q-icon name="water_drop" color="blue-7" size="sm" />
                  Resources Saved
                </div>
                <div class="resource-stats">
                  <div class="resource-stat">
                    <div class="resource-icon">
                      <q-icon name="water_drop" color="blue-7" size="lg" />
                    </div>
                    <div class="resource-details">
                      <div class="resource-value">{{ profile.total_water_saved.toFixed(0) }} L</div>
                      <div class="resource-label">Water Conserved</div>
                      <div class="text-caption text-grey-7">
                        {{ (profile.total_water_saved / 50).toFixed(0) }} showers worth
                      </div>
                    </div>
                  </div>
                  <q-separator class="q-my-md" />
                  <div class="resource-stat">
                    <div class="resource-icon">
                      <q-icon name="recycling" color="teal-7" size="lg" />
                    </div>
                    <div class="resource-details">
                      <div class="resource-value">{{ profile.total_plastic_saved.toFixed(1) }} kg</div>
                      <div class="resource-label">Plastic Prevented</div>
                      <div class="text-caption text-grey-7">
                        {{ (profile.total_plastic_saved / 0.014).toFixed(0) }} bottles avoided
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Badge Progress Preview -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Badge Progress</div>
          </div>
          <div class="col-12">
            <q-card flat bordered>
              <q-card-section>
                <div v-if="loadingBadgeProgress" class="text-center q-py-md">
                  <q-spinner color="primary" />
                </div>
                <div v-else-if="nearestBadges.length > 0">
                  <div class="text-subtitle2 text-grey-7 q-mb-md">Closest to Earning</div>
                  <div class="row q-col-gutter-md">
                    <div
                      v-for="progress in nearestBadges"
                      :key="progress.badge.id"
                      class="col-12 col-sm-6 col-md-4"
                    >
                      <q-card flat bordered class="badge-progress-card">
                        <q-card-section>
                          <div class="row items-center q-gutter-md">
                            <div class="col-auto">
                              <div class="badge-icon-medium" :style="{ color: progress.badge.color }">
                                {{ progress.badge.icon }}
                              </div>
                            </div>
                            <div class="col">
                              <div class="text-subtitle2 text-weight-bold">{{ progress.badge.name }}</div>
                              <div class="text-caption text-grey-7">
                                {{ progress.current_value.toFixed(1) }} / {{ progress.target_value.toFixed(1) }}
                              </div>
                              <q-linear-progress
                                :value="progress.progress_percentage / 100"
                                color="primary"
                                class="q-mt-xs"
                                rounded
                              />
                              <div class="text-caption text-primary q-mt-xs">
                                {{ progress.progress_percentage.toFixed(0) }}%
                              </div>
                            </div>
                          </div>
                        </q-card-section>
                      </q-card>
                    </div>
                  </div>
                  <div class="q-mt-md text-center">
                    <q-btn
                      flat
                      color="primary"
                      label="View All Badges"
                      icon="emoji_events"
                      :to="`/profile/${userId}`"
                    />
                  </div>
                </div>
                <div v-else class="text-center text-grey-7 q-py-md">
                  Make pledges to start earning badges!
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Recent Activity</div>
          </div>
          <div class="col-12">
            <q-card flat bordered>
              <q-card-section>
                <div v-if="loadingActivity" class="text-center q-py-md">
                  <q-spinner color="primary" />
                </div>
                <q-list v-else-if="recentActivities.length > 0" separator>
                  <q-item v-for="activity in recentActivities" :key="activity.id">
                    <q-item-section avatar>
                      <q-avatar :color="getActivityColor(activity.activity_type)" text-color="white">
                        <q-icon :name="getActivityIcon(activity.activity_type)" />
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ activity.activity_text }}</q-item-label>
                      <q-item-label caption>{{ formatDate(activity.created_at) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
                <div v-else class="text-center text-grey-7 q-py-md">
                  No recent activity
                </div>
                <div class="q-mt-md text-center">
                  <q-btn
                    flat
                    color="primary"
                    label="View Community Feed"
                    icon="people"
                    to="/community"
                  />
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="row q-col-gutter-md">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Quick Actions</div>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-btn
              unelevated
              color="primary"
              label="Make a Pledge"
              icon="add_circle"
              class="full-width"
              to="/pledge"
              size="lg"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-btn
              unelevated
              color="secondary"
              label="View Pledges"
              icon="list"
              class="full-width"
              to="/my-pledges"
              size="lg"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-btn
              unelevated
              color="accent"
              label="Share Story"
              icon="auto_stories"
              class="full-width"
              to="/stories"
              size="lg"
            />
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-btn
              unelevated
              color="info"
              label="View Impact"
              icon="insights"
              class="full-width"
              to="/impact"
              size="lg"
            />
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

export default defineComponent({
  name: 'DashboardPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const loadingBadgeProgress = ref(false)
    const loadingActivity = ref(false)
    const profile = ref(null)
    const badgeProgress = ref([])
    const recentActivities = ref([])

    // For demo purposes, using user ID 1. In production, get from auth
    const userId = ref(1)

    const completionRate = computed(() => {
      if (!profile.value || profile.value.total_pledges === 0) return 0
      return (profile.value.completed_pledges / profile.value.total_pledges) * 100
    })

    const nearestBadges = computed(() => {
      return badgeProgress.value
        .filter(p => !p.is_earned && p.progress_percentage > 0)
        .sort((a, b) => b.progress_percentage - a.progress_percentage)
        .slice(0, 3)
    })

    const loadProfile = async () => {
      loading.value = true
      try {
        const response = await api.get(`/api/users/${userId.value}/profile`)
        profile.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load dashboard'
        })
      } finally {
        loading.value = false
      }
    }

    const loadBadgeProgress = async () => {
      loadingBadgeProgress.value = true
      try {
        const response = await api.get(`/api/users/${userId.value}/badge-progress`)
        badgeProgress.value = response.data
      } catch (error) {
        console.error('Failed to load badge progress:', error)
      } finally {
        loadingBadgeProgress.value = false
      }
    }

    const loadRecentActivity = async () => {
      loadingActivity.value = true
      try {
        const response = await api.get('/api/activity/', {
          params: { limit: 5 }
        })
        recentActivities.value = response.data
      } catch (error) {
        console.error('Failed to load activity:', error)
      } finally {
        loadingActivity.value = false
      }
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

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)

      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      if (diffHours < 24) return `${diffHours}h ago`
      if (diffDays < 7) return `${diffDays}d ago`
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    onMounted(async () => {
      await loadProfile()
      await Promise.all([
        loadBadgeProgress(),
        loadRecentActivity()
      ])
    })

    return {
      loading,
      loadingBadgeProgress,
      loadingActivity,
      profile,
      badgeProgress,
      recentActivities,
      userId,
      completionRate,
      nearestBadges,
      getActivityIcon,
      getActivityColor,
      formatDate
    }
  }
})
</script>

<style scoped>
.stat-card {
  text-align: center;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

.stat-trend {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.impact-display {
  text-align: center;
  padding: 1.5rem 0;
}

.impact-value {
  font-size: 3rem;
  font-weight: bold;
  color: #2E7D32;
  line-height: 1;
}

.impact-unit {
  font-size: 1rem;
  color: #666;
  margin-top: 0.5rem;
}

.impact-comparison {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
}

.comparison-items {
  margin-top: 0.5rem;
}

.comparison-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  font-size: 0.875rem;
}

.progress-bar-container {
  height: 24px;
  background: #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  transition: width 0.5s ease;
  border-radius: 12px;
}

.resource-stats {
  padding: 1rem 0;
}

.resource-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.resource-icon {
  flex-shrink: 0;
}

.resource-details {
  flex-grow: 1;
}

.resource-value {
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1;
}

.resource-label {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.25rem;
}

.badge-icon-medium {
  font-size: 48px;
  line-height: 1;
}

.badge-progress-card {
  transition: transform 0.2s;
}

.badge-progress-card:hover {
  transform: translateY(-2px);
}
</style>
