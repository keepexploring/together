<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1400px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">Global Impact</h2>
      <p class="text-body1 q-mb-lg text-grey-7">
        See the collective impact of all pledges. Together, we're making a difference!
      </p>

      <!-- Loading State -->
      <div v-if="loading" class="flex flex-center" style="min-height: 400px;">
        <q-spinner-dots size="50px" color="primary" />
      </div>

      <!-- Impact Summary -->
      <div v-else>
        <!-- Stats Cards -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-primary text-white">
              <q-card-section>
                <div class="text-h4 text-weight-bold">{{ impact.total_pledges }}</div>
                <div class="text-subtitle2">Total Pledges</div>
                <q-icon name="check_circle" size="48px" class="absolute" style="right: 16px; top: 16px; opacity: 0.3;" />
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-secondary text-white">
              <q-card-section>
                <div class="text-h4 text-weight-bold">{{ impact.active_pledges }}</div>
                <div class="text-subtitle2">Active Pledges</div>
                <q-icon name="trending_up" size="48px" class="absolute" style="right: 16px; top: 16px; opacity: 0.3;" />
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-positive text-white">
              <q-card-section>
                <div class="text-h4 text-weight-bold">{{ impact.completed_pledges }}</div>
                <div class="text-subtitle2">Completed</div>
                <q-icon name="done_all" size="48px" class="absolute" style="right: 16px; top: 16px; opacity: 0.3;" />
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-accent text-white">
              <q-card-section>
                <div class="text-h4 text-weight-bold">{{ impact.total_participants }}</div>
                <div class="text-subtitle2">Participants</div>
                <q-icon name="groups" size="48px" class="absolute" style="right: 16px; top: 16px; opacity: 0.3;" />
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Impact Metrics -->
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="cloud" color="primary" size="48px" class="q-mr-md" />
                  <div>
                    <div class="text-h5 text-weight-bold">{{ formatNumber(impact.total_carbon_saved_kg) }} kg</div>
                    <div class="text-subtitle2 text-grey-7">CO₂ Saved</div>
                  </div>
                </div>
                <q-linear-progress :value="0.7" color="primary" class="q-mb-xs" />
                <div class="text-caption text-grey-6">
                  Equivalent to {{ (impact.total_carbon_saved_kg / 411).toFixed(1) }} car-free days
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="recycling" color="secondary" size="48px" class="q-mr-md" />
                  <div>
                    <div class="text-h5 text-weight-bold">{{ formatNumber(impact.total_plastic_saved_kg) }} kg</div>
                    <div class="text-subtitle2 text-grey-7">Plastic Prevented</div>
                  </div>
                </div>
                <q-linear-progress :value="0.6" color="secondary" class="q-mb-xs" />
                <div class="text-caption text-grey-6">
                  Equivalent to {{ Math.round(impact.total_plastic_saved_kg / 0.05) }} plastic bottles
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="water_drop" color="info" size="48px" class="q-mr-md" />
                  <div>
                    <div class="text-h5 text-weight-bold">{{ formatNumber(impact.total_water_saved_liters) }} L</div>
                    <div class="text-subtitle2 text-grey-7">Water Saved</div>
                  </div>
                </div>
                <q-linear-progress :value="0.8" color="info" class="q-mb-xs" />
                <div class="text-caption text-grey-6">
                  Equivalent to {{ Math.round(impact.total_water_saved_liters / 300) }} bathtubs
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="nature" color="positive" size="48px" class="q-mr-md" />
                  <div>
                    <div class="text-h5 text-weight-bold">{{ formatNumber(impact.total_trees_equivalent) }}</div>
                    <div class="text-subtitle2 text-grey-7">Tree Equivalents</div>
                  </div>
                </div>
                <q-linear-progress :value="0.5" color="positive" class="q-mb-xs" />
                <div class="text-caption text-grey-6">
                  Carbon absorption equivalent of {{ formatNumber(impact.total_trees_equivalent) }} trees
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Ecosystem Points -->
        <q-card flat bordered class="q-mt-md">
          <q-card-section>
            <div class="row items-center">
              <q-icon name="eco" color="accent" size="64px" class="q-mr-md" />
              <div>
                <div class="text-h4 text-weight-bold">{{ formatNumber(impact.total_ecosystem_points) }}</div>
                <div class="text-subtitle1 text-grey-7">Ecosystem Restoration Points</div>
                <div class="text-caption text-grey-6">
                  Combined impact from habitat creation, biodiversity support, and ecological restoration
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Motivational Message -->
        <q-card flat bordered class="q-mt-lg bg-primary text-white">
          <q-card-section>
            <div class="text-h5 text-center q-mb-md">
              <q-icon name="celebration" size="32px" class="q-mr-sm" />
              Together We Can Make a Difference!
            </div>
            <p class="text-center text-body1">
              Every action counts. Your pledges, combined with others around the world,
              create real, measurable impact for our planet. Keep going!
            </p>
          </q-card-section>
        </q-card>

        <!-- Organization Filter -->
        <div class="q-mt-xl">
          <h4 class="text-h5 q-mb-md">View Organization Impact</h4>
          <q-card flat bordered>
            <q-card-section>
              <div class="row q-col-gutter-md items-end">
                <div class="col-12 col-md-8">
                  <q-input
                    v-model="orgCode"
                    label="Enter Organization Code"
                    outlined
                    dense
                    hint="See the impact of a specific church or community group"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-btn
                    color="primary"
                    label="View"
                    icon="search"
                    @click="viewOrgImpact"
                    unelevated
                    :disable="!orgCode"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Organization Impact (if loaded) -->
        <div v-if="orgImpact" class="q-mt-lg">
          <q-card flat bordered class="bg-secondary text-white">
            <q-card-section>
              <h5 class="text-h5">{{ orgImpact.organization_name }}</h5>
              <div class="row q-col-gutter-md q-mt-md">
                <div class="col-12 col-sm-6 col-md-3">
                  <div class="text-h6">{{ orgImpact.total_pledges }}</div>
                  <div class="text-caption">Pledges</div>
                </div>
                <div class="col-12 col-sm-6 col-md-3">
                  <div class="text-h6">{{ formatNumber(orgImpact.total_carbon_saved_kg) }} kg</div>
                  <div class="text-caption">CO₂ Saved</div>
                </div>
                <div class="col-12 col-sm-6 col-md-3">
                  <div class="text-h6">{{ formatNumber(orgImpact.total_plastic_saved_kg) }} kg</div>
                  <div class="text-caption">Plastic Prevented</div>
                </div>
                <div class="col-12 col-sm-6 col-md-3">
                  <div class="text-h6">{{ formatNumber(orgImpact.total_water_saved_liters) }} L</div>
                  <div class="text-caption">Water Saved</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
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
  name: 'ImpactPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const impact = ref({
      total_carbon_saved_kg: 0,
      total_plastic_saved_kg: 0,
      total_water_saved_liters: 0,
      total_trees_equivalent: 0,
      total_ecosystem_points: 0,
      total_pledges: 0,
      active_pledges: 0,
      completed_pledges: 0,
      total_participants: 0
    })
    const orgCode = ref('')
    const orgImpact = ref(null)

    const fetchGlobalImpact = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/impact/global')
        impact.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load impact data'
        })
      } finally {
        loading.value = false
      }
    }

    const viewOrgImpact = async () => {
      if (!orgCode.value) return

      try {
        // First get org by code
        const orgResponse = await api.get(`/api/organizations/code/${orgCode.value}`)
        const org = orgResponse.data

        // Then get impact
        const impactResponse = await api.get(`/api/impact/organization/${org.id}`)
        orgImpact.value = impactResponse.data

        $q.notify({
          type: 'positive',
          message: `Loaded impact for ${orgImpact.value.organization_name}`
        })
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: error.response?.data?.detail || 'Organization not found'
        })
      }
    }

    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toFixed(1)
    }

    onMounted(() => {
      fetchGlobalImpact()
    })

    return {
      loading,
      impact,
      orgCode,
      orgImpact,
      viewOrgImpact,
      formatNumber
    }
  }
})
</script>

<style scoped>
.q-card {
  position: relative;
}
</style>
