<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1200px; margin: 0 auto;">
      <div class="row items-center q-mb-lg">
        <div class="col">
          <h2 class="text-h3 q-mb-sm">Environmental Campaigns</h2>
          <p class="text-body1 text-grey-7">
            Support campaigns for environmental issues and make your voice heard
          </p>
        </div>
        <div class="col-auto">
          <q-btn
            color="primary"
            label="Create Campaign"
            icon="add"
            @click="createDialog = true"
            unelevated
          />
        </div>
      </div>

      <!-- Campaigns List -->
      <div v-if="loading" class="flex flex-center" style="min-height: 400px;">
        <q-spinner-dots size="50px" color="primary" />
      </div>

      <div v-else class="row q-col-gutter-md">
        <div
          v-for="campaign in campaigns"
          :key="campaign.id"
          class="col-12 col-md-6"
        >
          <q-card flat bordered class="full-height">
            <q-card-section>
              <div class="row items-start">
                <q-icon
                  :name="getCategoryIcon(campaign.primary_category)"
                  :color="getCategoryColor(campaign.primary_category)"
                  size="36px"
                  class="q-mr-md"
                />
                <div class="col">
                  <div class="text-h6">{{ campaign.title }}</div>
                  <q-chip
                    :color="getCategoryColor(campaign.primary_category)"
                    text-color="white"
                    dense
                    size="sm"
                  >
                    {{ formatCategory(campaign.primary_category) }}
                  </q-chip>
                </div>
              </div>

              <p class="text-body2 q-mt-md">{{ campaign.description }}</p>

              <div class="q-mt-md">
                <div class="text-weight-bold text-grey-7 q-mb-xs">Goal:</div>
                <p class="text-body2">{{ campaign.goal }}</p>
              </div>

              <!-- Progress -->
              <div class="q-mt-md">
                <div class="row items-center q-mb-xs">
                  <div class="col">
                    <span class="text-weight-bold">{{ campaign.signature_count || 0 }}</span>
                    <span class="text-grey-7"> of {{ campaign.target_signatures }} signatures</span>
                  </div>
                  <div class="col-auto">
                    <span class="text-weight-bold">
                      {{ Math.round(((campaign.signature_count || 0) / campaign.target_signatures) * 100) }}%
                    </span>
                  </div>
                </div>
                <q-linear-progress
                  :value="(campaign.signature_count || 0) / campaign.target_signatures"
                  color="primary"
                  size="8px"
                />
              </div>
            </q-card-section>

            <q-card-actions>
              <q-btn
                color="primary"
                label="Sign Campaign"
                icon="edit"
                flat
                @click="signCampaign(campaign)"
              />
              <q-btn
                color="grey"
                label="View Details"
                flat
                :to="`/campaign/${campaign.id}`"
              />
            </q-card-actions>
          </q-card>
        </div>
      </div>

      <div v-if="!loading && campaigns.length === 0" class="text-center q-mt-xl">
        <q-icon name="campaign" size="64px" color="grey-5" />
        <p class="text-h6 text-grey-6 q-mt-md">No campaigns yet</p>
        <q-btn
          color="primary"
          label="Create the first campaign"
          @click="createDialog = true"
          unelevated
          class="q-mt-md"
        />
      </div>
    </div>

    <!-- Create Campaign Dialog -->
    <q-dialog v-model="createDialog" persistent>
      <q-card style="min-width: 600px">
        <q-card-section>
          <div class="text-h6">Create Environmental Campaign</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="submitCampaign">
            <q-input
              v-model="campaignForm.title"
              label="Campaign Title"
              outlined
              required
              class="q-mb-md"
            />

            <q-input
              v-model="campaignForm.description"
              label="Description"
              type="textarea"
              outlined
              required
              rows="3"
              class="q-mb-md"
            />

            <q-input
              v-model="campaignForm.goal"
              label="Campaign Goal"
              type="textarea"
              outlined
              required
              rows="2"
              class="q-mb-md"
              hint="What do you want to achieve?"
            />

            <q-select
              v-model="campaignForm.category"
              :options="categoryOptions"
              label="Primary Category"
              outlined
              required
              emit-value
              map-options
              class="q-mb-md"
            />

            <q-input
              v-model.number="campaignForm.targetSignatures"
              label="Target Signatures"
              type="number"
              outlined
              required
              class="q-mb-md"
            />

            <q-input
              v-model="campaignForm.creatorEmail"
              label="Your Email"
              type="email"
              outlined
              required
              class="q-mb-md"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="grey" v-close-popup />
          <q-btn
            unelevated
            label="Create Campaign"
            color="primary"
            @click="submitCampaign"
            :loading="submitting"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Sign Campaign Dialog -->
    <q-dialog v-model="signDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">Sign Campaign</div>
          <div class="text-subtitle2 text-grey-7">{{ selectedCampaign?.title }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="submitSignature">
            <q-input
              v-model="signatureForm.name"
              label="Your Name"
              outlined
              required
              class="q-mb-md"
            />

            <q-input
              v-model="signatureForm.email"
              label="Your Email"
              type="email"
              outlined
              required
              class="q-mb-md"
            />

            <q-input
              v-model="signatureForm.comment"
              label="Comment (Optional)"
              type="textarea"
              outlined
              rows="3"
              hint="Share why you support this campaign"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="grey" v-close-popup />
          <q-btn
            unelevated
            label="Sign Campaign"
            color="primary"
            @click="submitSignature"
            :loading="submitting"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'CampaignsPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const campaigns = ref([])
    const createDialog = ref(false)
    const signDialog = ref(false)
    const selectedCampaign = ref(null)
    const submitting = ref(false)

    const campaignForm = ref({
      title: '',
      description: '',
      goal: '',
      category: '',
      targetSignatures: 100,
      creatorEmail: ''
    })

    const signatureForm = ref({
      name: '',
      email: '',
      comment: ''
    })

    const categoryOptions = [
      { label: 'Carbon Reduction', value: 'carbon_reduction' },
      { label: 'Plastic Reduction', value: 'plastic_reduction' },
      { label: 'Water Conservation', value: 'water_conservation' },
      { label: 'Waste Reduction', value: 'waste_reduction' },
      { label: 'Ecosystem Restoration', value: 'ecosystem_restoration' },
      { label: 'Energy Conservation', value: 'energy_conservation' }
    ]

    const fetchCampaigns = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/campaigns/')
        campaigns.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load campaigns'
        })
      } finally {
        loading.value = false
      }
    }

    const submitCampaign = async () => {
      if (!campaignForm.value.title || !campaignForm.value.creatorEmail) {
        $q.notify({ type: 'warning', message: 'Please fill in required fields' })
        return
      }

      submitting.value = true
      try {
        await api.post('/api/campaigns/', {
          title: campaignForm.value.title,
          description: campaignForm.value.description,
          goal: campaignForm.value.goal,
          primary_category: campaignForm.value.category,
          target_signatures: campaignForm.value.targetSignatures
        }, {
          params: { creator_email: campaignForm.value.creatorEmail }
        })

        $q.notify({
          type: 'positive',
          message: 'Campaign created successfully!'
        })

        createDialog.value = false
        fetchCampaigns()
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: error.response?.data?.detail || 'Failed to create campaign'
        })
      } finally {
        submitting.value = false
      }
    }

    const signCampaign = (campaign) => {
      selectedCampaign.value = campaign
      signDialog.value = true
    }

    const submitSignature = async () => {
      if (!signatureForm.value.name || !signatureForm.value.email) {
        $q.notify({ type: 'warning', message: 'Please fill in required fields' })
        return
      }

      submitting.value = true
      try {
        await api.post(`/api/campaigns/${selectedCampaign.value.id}/sign`, {
          name: signatureForm.value.name,
          email: signatureForm.value.email,
          comment: signatureForm.value.comment
        })

        $q.notify({
          type: 'positive',
          message: 'Thank you for signing this campaign!'
        })

        signDialog.value = false
        signatureForm.value = { name: '', email: '', comment: '' }
        fetchCampaigns()
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: error.response?.data?.detail || 'Failed to sign campaign'
        })
      } finally {
        submitting.value = false
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
      fetchCampaigns()
    })

    return {
      loading,
      campaigns,
      createDialog,
      signDialog,
      selectedCampaign,
      campaignForm,
      signatureForm,
      submitting,
      categoryOptions,
      submitCampaign,
      signCampaign,
      submitSignature,
      getCategoryIcon,
      getCategoryColor,
      formatCategory
    }
  }
})
</script>
