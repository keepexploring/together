<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 1200px; width: 100%">
      <!-- Hero Section -->
      <div class="text-center q-mb-xl">
        <q-icon name="public" size="120px" color="primary" />
        <h1 class="text-h2 text-weight-bold q-mt-md q-mb-md">
          Planet Pledge
        </h1>
        <p class="text-h5 text-grey-7 q-mb-lg">
          Together we can restore and protect our planet
        </p>
        <p class="text-body1 q-mb-xl">
          Make pledges about how you'll reduce your impact on the planet.
          Join with your community, track your progress, and see the collective impact
          when we all work together.
        </p>

        <div class="row q-gutter-md justify-center">
          <q-btn
            size="lg"
            color="primary"
            label="Make a Pledge"
            icon="eco"
            to="/pledge"
            unelevated
          />
          <q-btn
            size="lg"
            color="secondary"
            label="View Impact"
            icon="insights"
            to="/impact"
            outline
          />
          <q-btn
            size="lg"
            color="accent"
            label="Browse Campaigns"
            icon="campaign"
            to="/campaigns"
            outline
          />
        </div>
      </div>

      <!-- Features Section -->
      <div class="row q-col-gutter-lg q-mt-xl">
        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="check_circle" size="64px" color="primary" />
              <h6 class="q-mt-md q-mb-sm">Make Pledges</h6>
              <p class="text-body2">
                Choose from 50+ scientifically-researched environmental actions,
                from everyday choices to creative solutions.
              </p>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="groups" size="64px" color="secondary" />
              <h6 class="q-mt-md q-mb-sm">Join Groups</h6>
              <p class="text-body2">
                Churches, community groups, and organizations can create
                simple codes for members to join and pledge together.
              </p>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="analytics" size="64px" color="accent" />
              <h6 class="q-mt-md q-mb-sm">Track Impact</h6>
              <p class="text-body2">
                See real-time calculations of carbon saved, plastic prevented,
                water conserved, and ecosystems restored.
              </p>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="campaign" size="64px" color="positive" />
              <h6 class="q-mt-md q-mb-sm">Launch Campaigns</h6>
              <p class="text-body2">
                Create environmental campaigns on issues you care about
                and gather signatures from the community.
              </p>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Global Impact Counters -->
      <div class="q-mt-xl">
        <h3 class="text-h4 text-center q-mb-lg">Collective Impact</h3>
        <p class="text-center text-grey-7 q-mb-lg">
          Real-time impact from our global community
        </p>
        <div class="row q-col-gutter-md">
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="impact-counter-card">
              <q-card-section class="text-center">
                <q-icon name="eco" size="48px" color="green-7" />
                <div class="counter-value text-green">{{ animatedCarbon }}</div>
                <div class="counter-label">kg CO₂ Saved</div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="impact-counter-card">
              <q-card-section class="text-center">
                <q-icon name="water_drop" size="48px" color="blue-7" />
                <div class="counter-value text-blue">{{ animatedWater }}</div>
                <div class="counter-label">Liters Water Saved</div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="impact-counter-card">
              <q-card-section class="text-center">
                <q-icon name="recycling" size="48px" color="teal-7" />
                <div class="counter-value text-teal">{{ animatedPlastic }}</div>
                <div class="counter-label">kg Plastic Prevented</div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-6 col-sm-3">
            <q-card flat bordered class="impact-counter-card">
              <q-card-section class="text-center">
                <q-icon name="people" size="48px" color="purple-7" />
                <div class="counter-value text-purple">{{ animatedParticipants }}</div>
                <div class="counter-label">Participants</div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Community Activity Feed -->
      <div class="q-mt-xl">
        <h3 class="text-h4 text-center q-mb-md">Community Activity</h3>
        <p class="text-center text-grey-7 q-mb-lg">
          See what others are doing to help the planet
        </p>
        <q-card flat bordered>
          <q-list v-if="recentActivities.length > 0" separator>
            <q-item v-for="activity in recentActivities" :key="activity.id">
              <q-item-section avatar>
                <q-avatar :color="getActivityColor(activity.activity_type)" text-color="white">
                  <q-icon :name="getActivityIcon(activity.activity_type)" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>
                  <span class="text-weight-bold">{{ activity.user.name }}</span>
                  {{ activity.activity_text }}
                </q-item-label>
                <q-item-label caption>{{ formatTimeAgo(activity.created_at) }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
          <q-card-section v-else class="text-center text-grey-7">
            <q-spinner v-if="loadingActivity" color="primary" />
            <div v-else>No activity yet. Be the first!</div>
          </q-card-section>
          <q-card-actions align="center" v-if="recentActivities.length > 0">
            <q-btn flat color="primary" label="View All Activity" icon="arrow_forward" to="/community" />
          </q-card-actions>
        </q-card>
      </div>

      <!-- Impact Categories -->
      <div class="q-mt-xl">
        <h3 class="text-h4 text-center q-mb-lg">Impact Categories</h3>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="cloud" size="48px" color="primary" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Carbon Reduction</div>
                    <div class="text-caption text-grey-7">
                      Transportation, diet, energy choices
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="recycling" size="48px" color="secondary" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Plastic Reduction</div>
                    <div class="text-caption text-grey-7">
                      Reusables, packaging, lifestyle changes
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="water_drop" size="48px" color="info" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Water Conservation</div>
                    <div class="text-caption text-grey-7">
                      Fixtures, habits, sustainable practices
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="delete" size="48px" color="warning" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Waste Reduction</div>
                    <div class="text-caption text-grey-7">
                      Composting, recycling, repair
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="nature" size="48px" color="positive" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Ecosystem Restoration</div>
                    <div class="text-caption text-grey-7">
                      Tree planting, habitat creation
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="bolt" size="48px" color="accent" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Energy Conservation</div>
                    <div class="text-caption text-grey-7">
                      Renewables, efficiency, smart choices
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="text-center q-mt-xl q-pa-xl bg-primary text-white" style="border-radius: 8px;">
        <h4 class="text-h4 q-mb-md">Ready to make a difference?</h4>
        <p class="text-body1 q-mb-lg">
          Join thousands of people making pledges to protect our planet
        </p>
        <q-btn
          size="lg"
          color="white"
          text-color="primary"
          label="Get Started"
          to="/pledge"
          unelevated
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'

export default defineComponent({
  name: 'IndexPage',

  setup() {
    const globalImpact = ref(null)
    const recentActivities = ref([])
    const loadingActivity = ref(false)
    const animatedCarbon = ref(0)
    const animatedWater = ref(0)
    const animatedPlastic = ref(0)
    const animatedParticipants = ref(0)

    const loadGlobalImpact = async () => {
      try {
        const response = await api.get('/api/impact/global')
        globalImpact.value = response.data

        // Animate counters
        animateCounter(animatedCarbon, globalImpact.value.total_carbon_saved_kg, 2000)
        animateCounter(animatedWater, globalImpact.value.total_water_saved_liters, 2000)
        animateCounter(animatedPlastic, globalImpact.value.total_plastic_saved_kg, 2000)
        animateCounter(animatedParticipants, globalImpact.value.total_participants, 2000)
      } catch (error) {
        console.error('Failed to load global impact:', error)
      }
    }

    const loadRecentActivity = async () => {
      loadingActivity.value = true
      try {
        const response = await api.get('/api/activity/', {
          params: { limit: 5, is_public: true }
        })
        recentActivities.value = response.data
      } catch (error) {
        console.error('Failed to load activity:', error)
      } finally {
        loadingActivity.value = false
      }
    }

    const animateCounter = (ref, target, duration) => {
      const start = 0
      const increment = target / (duration / 16) // ~60fps
      const timer = setInterval(() => {
        if (ref.value < target) {
          ref.value = Math.min(ref.value + increment, target)
        } else {
          ref.value = target
          clearInterval(timer)
        }
      }, 16)
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
      if (diffDays < 7) return `${diffDays}d ago`
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    onMounted(() => {
      loadGlobalImpact()
      loadRecentActivity()
    })

    return {
      globalImpact,
      recentActivities,
      loadingActivity,
      animatedCarbon: computed(() => Math.floor(animatedCarbon.value)),
      animatedWater: computed(() => Math.floor(animatedWater.value)),
      animatedPlastic: computed(() => Math.floor(animatedPlastic.value)),
      animatedParticipants: computed(() => Math.floor(animatedParticipants.value)),
      getActivityIcon,
      getActivityColor,
      formatTimeAgo
    }
  }
})
</script>

<style scoped>
.impact-counter-card {
  transition: transform 0.2s;
}

.impact-counter-card:hover {
  transform: translateY(-4px);
}

.counter-value {
  font-size: 2.5rem;
  font-weight: bold;
  line-height: 1.2;
  margin-top: 0.5rem;
}

.counter-label {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}
</style>
