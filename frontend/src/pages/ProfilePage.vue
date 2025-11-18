<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1200px; margin: 0 auto;">
      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
        <div class="text-subtitle1 q-mt-md">Loading profile...</div>
      </div>

      <!-- Profile Content -->
      <div v-else-if="profile">
        <!-- Profile Header -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <q-card flat bordered class="bg-gradient-primary text-white">
              <q-card-section class="q-pa-lg">
                <div class="row items-center">
                  <div class="col-auto">
                    <q-avatar size="100px" color="white" text-color="primary" class="text-h3">
                      {{ profile.user.name.charAt(0).toUpperCase() }}
                    </q-avatar>
                  </div>
                  <div class="col q-pl-lg">
                    <h2 class="text-h3 q-my-none">{{ profile.user.name }}</h2>
                    <p class="text-subtitle1 q-mb-sm opacity-90">{{ profile.user.email }}</p>
                    <div class="row q-gutter-md q-mt-md">
                      <div>
                        <div class="text-h6">{{ profile.total_pledges }}</div>
                        <div class="text-caption opacity-80">Total Pledges</div>
                      </div>
                      <div>
                        <div class="text-h6">{{ profile.badges_earned.length }}</div>
                        <div class="text-caption opacity-80">Badges Earned</div>
                      </div>
                      <div>
                        <div class="text-h6">{{ profile.current_streak_days }}</div>
                        <div class="text-caption opacity-80">Day Streak</div>
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Impact Summary -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Your Environmental Impact</div>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="eco" size="48px" color="green-7" />
                  <div class="text-h5 q-mt-sm">{{ profile.total_carbon_saved.toFixed(1) }} kg</div>
                  <div class="text-caption text-grey-7">Carbon Saved</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="water_drop" size="48px" color="blue-7" />
                  <div class="text-h5 q-mt-sm">{{ profile.total_water_saved.toFixed(0) }} L</div>
                  <div class="text-caption text-grey-7">Water Conserved</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="recycling" size="48px" color="teal-7" />
                  <div class="text-h5 q-mt-sm">{{ profile.total_plastic_saved.toFixed(1) }} kg</div>
                  <div class="text-caption text-grey-7">Plastic Prevented</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-center">
                  <q-icon name="task_alt" size="48px" color="purple-7" />
                  <div class="text-h5 q-mt-sm">{{ profile.completed_pledges }}</div>
                  <div class="text-caption text-grey-7">Pledges Completed</div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Badges Section -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12">
            <div class="text-h5 q-mb-md">
              Badges
              <q-chip color="primary" text-color="white">
                {{ profile.badges_earned.length }}
              </q-chip>
            </div>
          </div>

          <!-- Earned Badges -->
          <div class="col-12" v-if="profile.badges_earned.length > 0">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-md">Earned Badges</div>
                <div class="row q-col-gutter-md">
                  <div
                    v-for="userBadge in profile.badges_earned"
                    :key="userBadge.id"
                    class="col-6 col-sm-4 col-md-3 col-lg-2"
                  >
                    <q-card flat bordered class="badge-card cursor-pointer" @click="showBadgeDetails(userBadge.badge)">
                      <q-card-section class="text-center q-pa-md">
                        <div class="badge-icon" :style="{ color: userBadge.badge.color }">
                          {{ userBadge.badge.icon }}
                        </div>
                        <div class="text-caption text-weight-bold q-mt-sm">
                          {{ userBadge.badge.name }}
                        </div>
                        <div class="text-caption text-grey-7">
                          {{ formatBadgeTier(userBadge.badge.tier) }}
                        </div>
                        <!-- Physical Badge Order Button -->
                        <q-btn
                          v-if="userBadge.badge.can_order_physical && !userBadge.physical_ordered"
                          size="xs"
                          color="primary"
                          label="Order Physical"
                          class="q-mt-sm"
                          flat
                          dense
                          @click.stop="orderPhysicalBadge(userBadge)"
                        />
                        <q-chip
                          v-else-if="userBadge.physical_ordered"
                          size="xs"
                          color="green"
                          text-color="white"
                          class="q-mt-sm"
                        >
                          Ordered
                        </q-chip>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- No Badges Yet -->
          <div class="col-12" v-else>
            <q-banner rounded class="bg-blue-1">
              <template v-slot:avatar>
                <q-icon name="emoji_events" color="primary" />
              </template>
              Make pledges to start earning badges!
            </q-banner>
          </div>

          <!-- Badge Progress -->
          <div class="col-12">
            <q-btn
              flat
              color="primary"
              label="View All Badges & Progress"
              icon="emoji_events"
              @click="showBadgeProgress = true"
            />
          </div>
        </div>

        <!-- Recent Milestones -->
        <div class="row q-col-gutter-md q-mb-lg" v-if="profile.milestones.length > 0">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Recent Milestones</div>
          </div>
          <div class="col-12">
            <q-card flat bordered>
              <q-list separator>
                <q-item v-for="milestone in profile.milestones" :key="milestone.id">
                  <q-item-section avatar>
                    <q-avatar color="primary" text-color="white" icon="celebration" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="text-weight-bold">{{ milestone.title }}</q-item-label>
                    <q-item-label caption>{{ milestone.description }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-item-label caption>{{ formatDate(milestone.celebrated_at) }}</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card>
          </div>
        </div>

        <!-- Active Pledges -->
        <div class="row q-col-gutter-md">
          <div class="col-12">
            <div class="text-h5 q-mb-md">Active Pledges</div>
          </div>
          <div class="col-12">
            <q-btn
              color="primary"
              label="View All Pledges"
              icon="list"
              :to="'/my-pledges'"
              unelevated
            />
          </div>
        </div>
      </div>

      <!-- Badge Progress Dialog -->
      <q-dialog v-model="showBadgeProgress" maximized>
        <q-card>
          <q-bar class="bg-primary text-white">
            <div class="text-h6">Badge Progress</div>
            <q-space />
            <q-btn flat dense icon="close" v-close-popup />
          </q-bar>

          <q-card-section>
            <div v-if="loadingProgress" class="text-center q-py-xl">
              <q-spinner color="primary" size="3em" />
            </div>
            <div v-else>
              <q-tabs v-model="badgeTab" dense>
                <q-tab name="all" label="All Badges" />
                <q-tab name="carbon" label="Carbon" />
                <q-tab name="plastic" label="Plastic" />
                <q-tab name="water" label="Water" />
                <q-tab name="community" label="Community" />
                <q-tab name="commitment" label="Commitment" />
              </q-tabs>

              <q-tab-panels v-model="badgeTab" animated>
                <q-tab-panel
                  v-for="category in ['all', 'carbon', 'plastic', 'water', 'community', 'commitment']"
                  :key="category"
                  :name="category"
                >
                  <div class="row q-col-gutter-md">
                    <div
                      v-for="progress in getFilteredBadgeProgress(category)"
                      :key="progress.badge.id"
                      class="col-12 col-sm-6 col-md-4"
                    >
                      <q-card flat bordered :class="{ 'bg-green-1': progress.is_earned }">
                        <q-card-section>
                          <div class="row items-center">
                            <div class="col-auto">
                              <div class="badge-icon-large" :style="{ color: progress.badge.color }">
                                {{ progress.badge.icon }}
                              </div>
                            </div>
                            <div class="col">
                              <div class="text-subtitle1 text-weight-bold">{{ progress.badge.name }}</div>
                              <div class="text-caption text-grey-7">{{ progress.badge.description }}</div>
                              <div class="text-caption">
                                {{ progress.current_value.toFixed(1) }} / {{ progress.target_value.toFixed(1) }}
                              </div>
                              <q-linear-progress
                                :value="progress.progress_percentage / 100"
                                color="primary"
                                class="q-mt-sm"
                              />
                              <div class="text-caption q-mt-xs">
                                {{ progress.progress_percentage.toFixed(0) }}% Complete
                              </div>
                            </div>
                            <div class="col-auto" v-if="progress.is_earned">
                              <q-icon name="check_circle" color="green" size="md" />
                            </div>
                          </div>
                        </q-card-section>
                      </q-card>
                    </div>
                  </div>
                </q-tab-panel>
              </q-tab-panels>
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Badge Details Dialog -->
      <q-dialog v-model="showBadgeDetail" v-if="selectedBadge">
        <q-card style="min-width: 350px">
          <q-card-section class="text-center">
            <div class="badge-icon-huge" :style="{ color: selectedBadge.color }">
              {{ selectedBadge.icon }}
            </div>
            <div class="text-h5 q-mt-md">{{ selectedBadge.name }}</div>
            <div class="text-subtitle2 text-grey-7">{{ formatBadgeTier(selectedBadge.tier) }}</div>
            <div class="text-body1 q-mt-md">{{ selectedBadge.description }}</div>
          </q-card-section>
          <q-card-actions align="center">
            <q-btn flat label="Close" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useRoute } from 'vue-router'

export default defineComponent({
  name: 'ProfilePage',

  setup() {
    const $q = useQuasar()
    const route = useRoute()
    const loading = ref(true)
    const loadingProgress = ref(false)
    const profile = ref(null)
    const badgeProgress = ref([])
    const showBadgeProgress = ref(false)
    const showBadgeDetail = ref(false)
    const selectedBadge = ref(null)
    const badgeTab = ref('all')

    // For demo purposes, using user ID 1. In production, get from auth
    const userId = ref(route.params.userId || 1)

    const loadProfile = async () => {
      loading.value = true
      try {
        const response = await api.get(`/api/users/${userId.value}/profile`)
        profile.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load profile'
        })
      } finally {
        loading.value = false
      }
    }

    const loadBadgeProgress = async () => {
      loadingProgress.value = true
      try {
        const response = await api.get(`/api/users/${userId.value}/badge-progress`)
        badgeProgress.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load badge progress'
        })
      } finally {
        loadingProgress.value = false
      }
    }

    const showBadgeDetails = (badge) => {
      selectedBadge.value = badge
      showBadgeDetail.value = true
    }

    const orderPhysicalBadge = async (userBadge) => {
      try {
        await api.patch(`/api/users/${userId.value}/badges/${userBadge.badge.id}/order-physical`)
        $q.notify({
          type: 'positive',
          message: `Physical ${userBadge.badge.name} ordered! Cost: $${userBadge.badge.physical_cost.toFixed(2)}`
        })
        // Reload profile to update UI
        await loadProfile()
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to order physical badge'
        })
      }
    }

    const getFilteredBadgeProgress = (category) => {
      if (category === 'all') return badgeProgress.value
      return badgeProgress.value.filter(p => p.badge.category === category)
    }

    const formatBadgeTier = (tier) => {
      return tier.charAt(0).toUpperCase() + tier.slice(1)
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }

    onMounted(async () => {
      await loadProfile()
      showBadgeProgress.value = false
    })

    // Load badge progress when dialog opens
    const handleBadgeProgressOpen = async () => {
      if (badgeProgress.value.length === 0) {
        await loadBadgeProgress()
      }
    }

    return {
      loading,
      loadingProgress,
      profile,
      badgeProgress,
      showBadgeProgress,
      showBadgeDetail,
      selectedBadge,
      badgeTab,
      showBadgeDetails,
      orderPhysicalBadge,
      getFilteredBadgeProgress,
      formatBadgeTier,
      formatDate
    }
  },

  watch: {
    showBadgeProgress(newVal) {
      if (newVal && this.badgeProgress.length === 0) {
        this.loadBadgeProgress()
      }
    }
  },

  methods: {
    async loadBadgeProgress() {
      this.loadingProgress = true
      try {
        const response = await this.$axios.get(`/api/users/${this.userId}/badge-progress`)
        this.badgeProgress = response.data
      } catch (error) {
        this.$q.notify({
          type: 'negative',
          message: 'Failed to load badge progress'
        })
      } finally {
        this.loadingProgress = false
      }
    }
  }
})
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
}

.badge-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.badge-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.badge-icon {
  font-size: 48px;
  line-height: 1;
}

.badge-icon-large {
  font-size: 64px;
  line-height: 1;
}

.badge-icon-huge {
  font-size: 120px;
  line-height: 1;
}

.opacity-90 {
  opacity: 0.9;
}

.opacity-80 {
  opacity: 0.8;
}
</style>
