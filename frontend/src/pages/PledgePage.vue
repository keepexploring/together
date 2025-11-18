<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1400px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">Make Your Pledge</h2>
      <p class="text-body1 q-mb-lg text-grey-7">
        Choose an environmental action to commit to. All impact data is based on scientific research.
      </p>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-lg">
        <q-card-section>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-select
                v-model="selectedCategory"
                :options="categoryOptions"
                label="Filter by Category"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-6">
              <q-input
                v-model="searchQuery"
                label="Search actions"
                outlined
                dense
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Actions Grid -->
      <div class="row q-col-gutter-md">
        <div
          v-for="action in filteredActions"
          :key="action.id"
          class="col-12 col-md-6 col-lg-4"
        >
          <q-card flat bordered class="full-height action-card" @click="selectAction(action)">
            <q-card-section>
              <div class="row items-start">
                <q-icon
                  :name="getCategoryIcon(action.category)"
                  :color="getCategoryColor(action.category)"
                  size="36px"
                  class="q-mr-md"
                />
                <div class="col">
                  <div class="text-h6">{{ action.title }}</div>
                  <q-chip
                    :color="getCategoryColor(action.category)"
                    text-color="white"
                    dense
                    size="sm"
                  >
                    {{ formatCategory(action.category) }}
                  </q-chip>
                </div>
              </div>

              <p class="text-body2 q-mt-md">{{ action.description }}</p>

              <!-- Impact Preview -->
              <div class="q-mt-md">
                <div class="text-caption text-weight-bold text-grey-7 q-mb-xs">Impact per {{ action.frequency_type }}:</div>
                <div class="impact-items">
                  <div v-if="action.carbon_saved_kg > 0" class="impact-item">
                    <q-icon name="cloud" size="xs" color="primary" />
                    <span class="text-caption">{{ action.carbon_saved_kg }} kg CO₂</span>
                  </div>
                  <div v-if="action.plastic_saved_kg > 0" class="impact-item">
                    <q-icon name="recycling" size="xs" color="secondary" />
                    <span class="text-caption">{{ action.plastic_saved_kg }} kg plastic</span>
                  </div>
                  <div v-if="action.water_saved_liters > 0" class="impact-item">
                    <q-icon name="water_drop" size="xs" color="info" />
                    <span class="text-caption">{{ action.water_saved_liters }} L water</span>
                  </div>
                  <div v-if="action.trees_equivalent > 0" class="impact-item">
                    <q-icon name="nature" size="xs" color="positive" />
                    <span class="text-caption">{{ action.trees_equivalent }} trees</span>
                  </div>
                </div>
              </div>
            </q-card-section>

            <q-card-actions>
              <q-btn
                color="primary"
                label="I'll do this!"
                icon="check_circle"
                flat
                @click.stop="selectAction(action)"
              />
            </q-card-actions>
          </q-card>
        </div>
      </div>

      <div v-if="filteredActions.length === 0" class="text-center q-mt-xl">
        <q-icon name="search_off" size="64px" color="grey-5" />
        <p class="text-h6 text-grey-6 q-mt-md">No actions found</p>
      </div>
    </div>

    <!-- Pledge Dialog -->
    <q-dialog v-model="pledgeDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">Make Your Pledge</div>
          <div class="text-subtitle2 text-grey-7">{{ selectedAction?.title }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="submitPledge">
            <q-input
              v-model="pledgeForm.name"
              label="Your Name"
              outlined
              required
              class="q-mb-md"
            />

            <q-input
              v-model="pledgeForm.email"
              label="Your Email"
              type="email"
              outlined
              required
              class="q-mb-md"
              hint="We'll use this to follow up on your progress (honor system!)"
            />

            <q-input
              v-model="pledgeForm.accessCode"
              label="Group Access Code (Optional)"
              outlined
              class="q-mb-md"
              hint="If you're joining with a group, enter their code"
            />

            <q-input
              v-model.number="pledgeForm.durationDays"
              label="Duration (days)"
              type="number"
              outlined
              required
              class="q-mb-md"
              :rules="[val => val > 0 || 'Must be positive']"
            />

            <q-input
              v-model.number="pledgeForm.followUpDays"
              label="Check-in every (days)"
              type="number"
              outlined
              required
              class="q-mb-md"
              hint="How often should we check on your progress?"
              :rules="[val => val > 0 || 'Must be positive']"
            />

            <q-input
              v-model="pledgeForm.commitment"
              label="Personal Commitment (Optional)"
              type="textarea"
              outlined
              rows="3"
              hint="Add your own notes or specific goals"
            />

            <div class="q-mt-md q-pa-md bg-grey-2" style="border-radius: 4px;">
              <div class="text-caption text-weight-bold q-mb-xs">Your projected impact:</div>
              <div v-if="selectedAction">
                <div v-if="calculatedImpact.carbon > 0">
                  <q-icon name="cloud" color="primary" size="xs" />
                  {{ calculatedImpact.carbon.toFixed(2) }} kg CO₂ saved
                </div>
                <div v-if="calculatedImpact.plastic > 0">
                  <q-icon name="recycling" color="secondary" size="xs" />
                  {{ calculatedImpact.plastic.toFixed(2) }} kg plastic prevented
                </div>
                <div v-if="calculatedImpact.water > 0">
                  <q-icon name="water_drop" color="info" size="xs" />
                  {{ calculatedImpact.water.toFixed(2) }} liters water saved
                </div>
              </div>
            </div>
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="grey" v-close-popup />
          <q-btn
            unelevated
            label="Make Pledge"
            color="primary"
            @click="submitPledge"
            :loading="submitting"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'PledgePage',

  setup() {
    const $q = useQuasar()
    const router = useRouter()
    const actions = ref([])
    const selectedCategory = ref(null)
    const searchQuery = ref('')
    const pledgeDialog = ref(false)
    const selectedAction = ref(null)
    const submitting = ref(false)

    const pledgeForm = ref({
      name: '',
      email: '',
      accessCode: '',
      durationDays: 30,
      followUpDays: 7,
      commitment: ''
    })

    const categoryOptions = [
      { label: 'Carbon Reduction', value: 'carbon_reduction' },
      { label: 'Plastic Reduction', value: 'plastic_reduction' },
      { label: 'Water Conservation', value: 'water_conservation' },
      { label: 'Waste Reduction', value: 'waste_reduction' },
      { label: 'Ecosystem Restoration', value: 'ecosystem_restoration' },
      { label: 'Energy Conservation', value: 'energy_conservation' }
    ]

    const filteredActions = computed(() => {
      let filtered = actions.value

      if (selectedCategory.value) {
        filtered = filtered.filter(a => a.category === selectedCategory.value)
      }

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(a =>
          a.title.toLowerCase().includes(query) ||
          a.description.toLowerCase().includes(query)
        )
      }

      return filtered
    })

    const calculatedImpact = computed(() => {
      if (!selectedAction.value) return { carbon: 0, plastic: 0, water: 0 }

      const days = pledgeForm.value.durationDays
      let multiplier = days / 365.0

      const freq = selectedAction.value.frequency_type
      if (freq === 'daily') multiplier *= 365
      else if (freq === 'weekly') multiplier *= 52
      else if (freq === 'monthly') multiplier *= 12
      else if (freq === 'once') multiplier = 1

      return {
        carbon: selectedAction.value.carbon_saved_kg * multiplier,
        plastic: selectedAction.value.plastic_saved_kg * multiplier,
        water: selectedAction.value.water_saved_liters * multiplier
      }
    })

    const fetchActions = async () => {
      try {
        const response = await api.get('/api/actions/')
        actions.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load actions'
        })
      }
    }

    const selectAction = (action) => {
      selectedAction.value = action
      pledgeDialog.value = true
    }

    const submitPledge = async () => {
      if (!pledgeForm.value.name || !pledgeForm.value.email) {
        $q.notify({ type: 'warning', message: 'Please fill in required fields' })
        return
      }

      submitting.value = true
      try {
        const payload = {
          user_name: pledgeForm.value.name,
          user_email: pledgeForm.value.email,
          action_id: selectedAction.value.id,
          commitment_text: pledgeForm.value.commitment,
          duration_days: pledgeForm.value.durationDays,
          follow_up_frequency_days: pledgeForm.value.followUpDays
        }

        let response
        if (pledgeForm.value.accessCode) {
          response = await api.post('/api/pledges/simple', {
            access_code: pledgeForm.value.accessCode,
            ...payload
          })
        } else {
          response = await api.post('/api/pledges/', payload)
        }

        $q.notify({
          type: 'positive',
          message: 'Pledge created successfully! Together we make a difference.',
          timeout: 3000
        })

        pledgeDialog.value = false
        resetForm()

        router.push('/impact')
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: error.response?.data?.detail || 'Failed to create pledge'
        })
      } finally {
        submitting.value = false
      }
    }

    const resetForm = () => {
      pledgeForm.value = {
        name: '',
        email: '',
        accessCode: '',
        durationDays: 30,
        followUpDays: 7,
        commitment: ''
      }
    }

    const getCategoryIcon = (category) => {
      const icons = {
        carbon_reduction: 'cloud',
        plastic_reduction: 'recycling',
        water_conservation: 'water_drop',
        waste_reduction: 'delete',
        ecosystem_restoration: 'nature',
        energy_conservation: 'bolt'
      }
      return icons[category] || 'eco'
    }

    const getCategoryColor = (category) => {
      const colors = {
        carbon_reduction: 'primary',
        plastic_reduction: 'secondary',
        water_conservation: 'info',
        waste_reduction: 'warning',
        ecosystem_restoration: 'positive',
        energy_conservation: 'accent'
      }
      return colors[category] || 'primary'
    }

    const formatCategory = (category) => {
      return category.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
    }

    onMounted(() => {
      fetchActions()
    })

    return {
      actions,
      selectedCategory,
      searchQuery,
      pledgeDialog,
      selectedAction,
      pledgeForm,
      submitting,
      categoryOptions,
      filteredActions,
      calculatedImpact,
      selectAction,
      submitPledge,
      getCategoryIcon,
      getCategoryColor,
      formatCategory
    }
  }
})
</script>

<style scoped>
.action-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.impact-items {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.impact-item {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(0,0,0,0.05);
  padding: 4px 8px;
  border-radius: 4px;
}
</style>
