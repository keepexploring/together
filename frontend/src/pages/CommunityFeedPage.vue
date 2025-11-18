<template>
  <q-page class="q-pa-md">
    <div style="max-width: 900px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">Community Activity</h2>
      <p class="text-subtitle1 q-mb-lg text-grey-7">
        See what others are doing to help the planet
      </p>

      <!-- Filter Options -->
      <div class="row q-col-gutter-md q-mb-lg">
        <div class="col-12 col-sm-6">
          <q-select
            v-model="activityFilter"
            :options="filterOptions"
            label="Filter by Type"
            outlined
            dense
            emit-value
            map-options
            @update:model-value="loadActivities"
          />
        </div>
        <div class="col-12 col-sm-6">
          <q-btn
            flat
            color="primary"
            label="Refresh"
            icon="refresh"
            @click="loadActivities"
            class="full-width"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
        <div class="text-subtitle1 q-mt-md">Loading community activity...</div>
      </div>

      <!-- Activity Feed -->
      <div v-else>
        <!-- Activity Cards -->
        <q-card v-if="activities.length > 0" flat bordered>
          <q-list separator>
            <q-item
              v-for="activity in activities"
              :key="activity.id"
              class="activity-item"
            >
              <q-item-section avatar>
                <q-avatar :color="getActivityColor(activity.activity_type)" text-color="white" size="56px">
                  <q-icon :name="getActivityIcon(activity.activity_type)" size="md" />
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label class="text-body1">
                  <span class="text-weight-bold">{{ activity.user.name }}</span>
                  {{ getActivityVerb(activity.activity_type) }}
                </q-item-label>
                <q-item-label class="text-body2 q-mt-xs">
                  {{ activity.activity_text }}
                </q-item-label>
                <q-item-label caption class="q-mt-xs">
                  <q-icon name="schedule" size="xs" /> {{ formatDate(activity.created_at) }}
                </q-item-label>
              </q-item-section>

              <q-item-section side>
                <div class="activity-actions">
                  <q-btn
                    flat
                    round
                    dense
                    icon="thumb_up_alt"
                    size="sm"
                    color="grey-6"
                    @click="likeActivity(activity)"
                  >
                    <q-tooltip>Encourage</q-tooltip>
                  </q-btn>
                </div>
              </q-item-section>
            </q-item>
          </q-list>

          <!-- Load More -->
          <q-card-section v-if="hasMore" class="text-center">
            <q-btn
              flat
              color="primary"
              label="Load More"
              icon="expand_more"
              @click="loadMore"
              :loading="loadingMore"
            />
          </q-card-section>
        </q-card>

        <!-- Empty State -->
        <q-card v-else flat bordered class="text-center q-py-xl">
          <q-card-section>
            <q-icon name="people_outline" size="64px" color="grey-5" />
            <div class="text-h6 q-mt-md text-grey-7">No activity yet</div>
            <div class="text-body2 text-grey-6 q-mt-sm">
              Be the first to make a pledge and inspire others!
            </div>
            <q-btn
              color="primary"
              label="Make a Pledge"
              icon="add"
              to="/pledge"
              class="q-mt-md"
              unelevated
            />
          </q-card-section>
        </q-card>

        <!-- Community Stats -->
        <div class="row q-col-gutter-md q-mt-lg">
          <div class="col-12">
            <div class="text-h6 q-mb-md">Community Impact</div>
          </div>
          <div class="col-12">
            <q-card flat bordered>
              <q-card-section>
                <div v-if="loadingStats" class="text-center q-py-md">
                  <q-spinner color="primary" />
                </div>
                <div v-else-if="communityStats" class="row q-col-gutter-md">
                  <div class="col-6 col-sm-3 text-center">
                    <div class="community-stat-value text-primary">
                      {{ communityStats.total_pledges }}
                    </div>
                    <div class="community-stat-label">Total Pledges</div>
                  </div>
                  <div class="col-6 col-sm-3 text-center">
                    <div class="community-stat-value text-green">
                      {{ communityStats.total_participants }}
                    </div>
                    <div class="community-stat-label">Participants</div>
                  </div>
                  <div class="col-6 col-sm-3 text-center">
                    <div class="community-stat-value text-blue">
                      {{ communityStats.total_carbon_saved_kg.toFixed(0) }} kg
                    </div>
                    <div class="community-stat-label">Carbon Saved</div>
                  </div>
                  <div class="col-6 col-sm-3 text-center">
                    <div class="community-stat-value text-teal">
                      {{ communityStats.total_water_saved_liters.toFixed(0) }} L
                    </div>
                    <div class="community-stat-label">Water Saved</div>
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
import { defineComponent, ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'CommunityFeedPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const loadingMore = ref(false)
    const loadingStats = ref(false)
    const activities = ref([])
    const communityStats = ref(null)
    const activityFilter = ref('all')
    const skip = ref(0)
    const limit = ref(20)
    const hasMore = ref(true)

    const filterOptions = [
      { label: 'All Activity', value: 'all' },
      { label: 'Pledges Created', value: 'pledge_created' },
      { label: 'Pledges Completed', value: 'pledge_completed' },
      { label: 'Badges Earned', value: 'badge_earned' },
      { label: 'Milestones Reached', value: 'milestone_reached' }
    ]

    const loadActivities = async (append = false) => {
      if (!append) {
        loading.value = true
        skip.value = 0
        activities.value = []
      } else {
        loadingMore.value = true
      }

      try {
        const response = await api.get('/api/activity/', {
          params: {
            skip: skip.value,
            limit: limit.value,
            is_public: true
          }
        })

        if (append) {
          activities.value.push(...response.data)
        } else {
          activities.value = response.data
        }

        hasMore.value = response.data.length === limit.value
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load community activity'
        })
      } finally {
        loading.value = false
        loadingMore.value = false
      }
    }

    const loadCommunityStats = async () => {
      loadingStats.value = true
      try {
        const response = await api.get('/api/impact/global')
        communityStats.value = response.data
      } catch (error) {
        console.error('Failed to load community stats:', error)
      } finally {
        loadingStats.value = false
      }
    }

    const loadMore = () => {
      skip.value += limit.value
      loadActivities(true)
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

    const getActivityVerb = (type) => {
      const verbs = {
        pledge_created: '',
        pledge_completed: '',
        badge_earned: '',
        milestone_reached: ''
      }
      return verbs[type] || ''
    }

    const likeActivity = (activity) => {
      $q.notify({
        type: 'positive',
        message: 'Encouragement sent!',
        icon: 'thumb_up',
        timeout: 1000
      })
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)

      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins} minutes ago`
      if (diffHours < 24) return `${diffHours} hours ago`
      if (diffDays < 7) return `${diffDays} days ago`
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }

    onMounted(async () => {
      await Promise.all([
        loadActivities(),
        loadCommunityStats()
      ])
    })

    return {
      loading,
      loadingMore,
      loadingStats,
      activities,
      communityStats,
      activityFilter,
      filterOptions,
      hasMore,
      loadActivities,
      loadMore,
      getActivityIcon,
      getActivityColor,
      getActivityVerb,
      likeActivity,
      formatDate
    }
  }
})
</script>

<style scoped>
.activity-item {
  transition: background-color 0.2s;
}

.activity-item:hover {
  background-color: #f5f5f5;
}

.activity-actions {
  display: flex;
  gap: 0.5rem;
}

.community-stat-value {
  font-size: 2rem;
  font-weight: bold;
  line-height: 1;
}

.community-stat-label {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}
</style>
