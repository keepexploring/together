<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1200px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">Organization Leaderboards</h2>
      <p class="text-subtitle1 q-mb-lg text-grey-7">
        See which organizations are leading the way in environmental action
      </p>

      <!-- Metric Selection -->
      <div class="row q-col-gutter-md q-mb-lg">
        <div class="col-12 col-sm-6 col-md-3">
          <q-select
            v-model="rankingMetric"
            :options="metricOptions"
            label="Rank By"
            outlined
            dense
            emit-value
            map-options
            @update:model-value="loadLeaderboard"
          />
        </div>
        <div class="col-12 col-sm-6 col-md-3">
          <q-select
            v-model="timeframe"
            :options="timeframeOptions"
            label="Timeframe"
            outlined
            dense
            emit-value
            map-options
            @update:model-value="loadLeaderboard"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
      </div>

      <!-- Leaderboard -->
      <div v-else-if="organizations.length > 0">
        <!-- Top 3 Podium -->
        <div class="row q-col-gutter-md q-mb-lg">
          <div v-for="(org, index) in topThree" :key="org.id" class="col-12 col-md-4">
            <q-card
              flat
              bordered
              :class="[
                'podium-card',
                index === 0 ? 'gold-card' : index === 1 ? 'silver-card' : 'bronze-card'
              ]"
            >
              <q-card-section class="text-center">
                <div class="podium-rank">
                  <q-icon
                    :name="index === 0 ? 'emoji_events' : 'military_tech'"
                    size="64px"
                    :color="index === 0 ? 'amber' : index === 1 ? 'grey-6' : 'orange-8'"
                  />
                  <div class="rank-number">#{{ index + 1 }}</div>
                </div>
                <div class="text-h5 q-mt-md">{{ org.organization_name }}</div>
                <div class="text-h6 text-weight-bold q-mt-sm" :class="`text-${getMetricColor()}`">
                  {{ formatMetricValue(getMetricValue(org)) }}
                </div>
                <div class="text-caption text-grey-7">{{ getMetricLabel() }}</div>
                <q-separator class="q-my-md" />
                <div class="row q-col-gutter-sm text-center">
                  <div class="col-4">
                    <div class="text-weight-bold">{{ org.total_pledges }}</div>
                    <div class="text-caption">Pledges</div>
                  </div>
                  <div class="col-4">
                    <div class="text-weight-bold">{{ org.total_participants }}</div>
                    <div class="text-caption">Members</div>
                  </div>
                  <div class="col-4">
                    <div class="text-weight-bold">{{ org.active_pledges }}</div>
                    <div class="text-caption">Active</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Full Rankings Table -->
        <q-card flat bordered>
          <q-card-section>
            <div class="text-h6 q-mb-md">Full Rankings</div>
            <q-table
              :rows="organizations"
              :columns="columns"
              row-key="organization_id"
              flat
              :pagination="{ rowsPerPage: 10 }"
            >
              <template v-slot:body-cell-rank="props">
                <q-td :props="props">
                  <q-badge :color="getRankColor(props.rowIndex + 1)" text-color="white">
                    #{{ props.rowIndex + 1 }}
                  </q-badge>
                </q-td>
              </template>

              <template v-slot:body-cell-organization_name="props">
                <q-td :props="props">
                  <div class="text-weight-bold">{{ props.value }}</div>
                </q-td>
              </template>

              <template v-slot:body-cell-carbon="props">
                <q-td :props="props">
                  <div class="row items-center q-gutter-xs">
                    <q-icon name="eco" color="green" size="sm" />
                    <span>{{ props.value.toFixed(1) }} kg</span>
                  </div>
                </q-td>
              </template>

              <template v-slot:body-cell-water="props">
                <q-td :props="props">
                  <div class="row items-center q-gutter-xs">
                    <q-icon name="water_drop" color="blue" size="sm" />
                    <span>{{ props.value.toFixed(0) }} L</span>
                  </div>
                </q-td>
              </template>

              <template v-slot:body-cell-plastic="props">
                <q-td :props="props">
                  <div class="row items-center q-gutter-xs">
                    <q-icon name="recycling" color="teal" size="sm" />
                    <span>{{ props.value.toFixed(1) }} kg</span>
                  </div>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>

        <!-- Impact Insights -->
        <div class="row q-col-gutter-md q-mt-lg">
          <div class="col-12">
            <div class="text-h6 q-mb-md">Community Impact Insights</div>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="groups" size="48px" color="primary" />
                <div class="text-h6 q-mt-sm">{{ totalOrganizations }}</div>
                <div class="text-caption text-grey-7">Organizations</div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="people" size="48px" color="blue" />
                <div class="text-h6 q-mt-sm">{{ totalParticipants }}</div>
                <div class="text-caption text-grey-7">Total Participants</div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="trending_up" size="48px" color="green" />
                <div class="text-h6 q-mt-sm">{{ averagePledgesPerOrg }}</div>
                <div class="text-caption text-grey-7">Avg Pledges/Org</div>
              </q-card-section>
            </q-card>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered>
              <q-card-section class="text-center">
                <q-icon name="emoji_events" size="48px" color="amber" />
                <div class="text-h6 q-mt-sm">{{ leadingOrg }}</div>
                <div class="text-caption text-grey-7">Leading Org</div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <q-card v-else flat bordered class="text-center q-py-xl">
        <q-card-section>
          <q-icon name="leaderboard" size="64px" color="grey-5" />
          <div class="text-h6 q-mt-md text-grey-7">No organizations yet</div>
          <div class="text-body2 text-grey-6 q-mt-sm">
            Be the first to create an organization!
          </div>
          <q-btn
            color="primary"
            label="Create Organization"
            icon="add"
            to="/organize"
            class="q-mt-md"
            unelevated
          />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'LeaderboardsPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const organizations = ref([])
    const rankingMetric = ref('carbon')
    const timeframe = ref('all')

    const metricOptions = [
      { label: 'Carbon Saved', value: 'carbon' },
      { label: 'Water Conserved', value: 'water' },
      { label: 'Plastic Prevented', value: 'plastic' },
      { label: 'Total Pledges', value: 'pledges' },
      { label: 'Active Members', value: 'members' }
    ]

    const timeframeOptions = [
      { label: 'All Time', value: 'all' },
      { label: 'This Month', value: 'month' },
      { label: 'This Week', value: 'week' }
    ]

    const columns = [
      { name: 'rank', label: 'Rank', field: 'rank', align: 'center' },
      { name: 'organization_name', label: 'Organization', field: 'organization_name', align: 'left' },
      { name: 'carbon', label: 'Carbon Saved', field: 'total_carbon_saved_kg', align: 'center', sortable: true },
      { name: 'water', label: 'Water Saved', field: 'total_water_saved_liters', align: 'center', sortable: true },
      { name: 'plastic', label: 'Plastic Prevented', field: 'total_plastic_saved_kg', align: 'center', sortable: true },
      { name: 'total_pledges', label: 'Pledges', field: 'total_pledges', align: 'center', sortable: true },
      { name: 'total_participants', label: 'Members', field: 'total_participants', align: 'center', sortable: true }
    ]

    const topThree = computed(() => organizations.value.slice(0, 3))

    const totalOrganizations = computed(() => organizations.value.length)

    const totalParticipants = computed(() => {
      return organizations.value.reduce((sum, org) => sum + org.total_participants, 0)
    })

    const averagePledgesPerOrg = computed(() => {
      if (organizations.value.length === 0) return 0
      const total = organizations.value.reduce((sum, org) => sum + org.total_pledges, 0)
      return Math.round(total / organizations.value.length)
    })

    const leadingOrg = computed(() => {
      if (organizations.value.length === 0) return 'N/A'
      return organizations.value[0].organization_name
    })

    const loadLeaderboard = async () => {
      loading.value = true
      try {
        // Get all organizations
        const orgsResponse = await api.get('/api/organizations/')
        const allOrgs = orgsResponse.data

        // Get impact for each organization
        const orgImpacts = await Promise.all(
          allOrgs.map(async (org) => {
            try {
              const impactResponse = await api.get(`/api/impact/organization/${org.id}`)
              return impactResponse.data
            } catch (error) {
              return {
                organization_id: org.id,
                organization_name: org.name,
                total_carbon_saved_kg: 0,
                total_plastic_saved_kg: 0,
                total_water_saved_liters: 0,
                total_pledges: 0,
                total_participants: 0,
                active_pledges: 0
              }
            }
          })
        )

        // Sort based on selected metric
        organizations.value = orgImpacts.sort((a, b) => {
          const aValue = getMetricValue(a)
          const bValue = getMetricValue(b)
          return bValue - aValue
        })
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load leaderboard'
        })
      } finally {
        loading.value = false
      }
    }

    const getMetricValue = (org) => {
      switch (rankingMetric.value) {
        case 'carbon':
          return org.total_carbon_saved_kg
        case 'water':
          return org.total_water_saved_liters
        case 'plastic':
          return org.total_plastic_saved_kg
        case 'pledges':
          return org.total_pledges
        case 'members':
          return org.total_participants
        default:
          return 0
      }
    }

    const getMetricLabel = () => {
      const option = metricOptions.find(o => o.value === rankingMetric.value)
      return option ? option.label : ''
    }

    const getMetricColor = () => {
      switch (rankingMetric.value) {
        case 'carbon': return 'green'
        case 'water': return 'blue'
        case 'plastic': return 'teal'
        default: return 'primary'
      }
    }

    const formatMetricValue = (value) => {
      if (rankingMetric.value === 'carbon' || rankingMetric.value === 'plastic') {
        return `${value.toFixed(1)} kg`
      }
      if (rankingMetric.value === 'water') {
        return `${value.toFixed(0)} L`
      }
      return Math.round(value)
    }

    const getRankColor = (rank) => {
      if (rank === 1) return 'amber'
      if (rank === 2) return 'grey-6'
      if (rank === 3) return 'orange-8'
      if (rank <= 5) return 'primary'
      return 'grey-7'
    }

    onMounted(() => {
      loadLeaderboard()
    })

    return {
      loading,
      organizations,
      rankingMetric,
      timeframe,
      metricOptions,
      timeframeOptions,
      columns,
      topThree,
      totalOrganizations,
      totalParticipants,
      averagePledgesPerOrg,
      leadingOrg,
      loadLeaderboard,
      getMetricValue,
      getMetricLabel,
      getMetricColor,
      formatMetricValue,
      getRankColor
    }
  }
})
</script>

<style scoped>
.podium-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.podium-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.gold-card {
  border-top: 4px solid #FFD700;
}

.silver-card {
  border-top: 4px solid #C0C0C0;
}

.bronze-card {
  border-top: 4px solid #CD7F32;
}

.podium-rank {
  position: relative;
}

.rank-number {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
</style>
