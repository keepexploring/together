<template>
  <q-page class="q-pa-md">
    <div style="max-width: 900px; margin: 0 auto;">
      <q-btn flat icon="arrow_back" label="Back" @click="$router.back()" class="q-mb-md" />

      <div v-if="campaign">
        <h2 class="text-h3 q-mb-md">{{ campaign.title }}</h2>

        <q-card flat bordered class="q-mb-md">
          <q-card-section>
            <p class="text-body1">{{ campaign.description }}</p>
            <div class="q-mt-md">
              <div class="text-weight-bold">Goal:</div>
              <p>{{ campaign.goal }}</p>
            </div>
          </q-card-section>
        </q-card>

        <q-card flat bordered>
          <q-card-section>
            <div class="text-h6 q-mb-md">
              {{ campaign.signature_count || 0 }} / {{ campaign.target_signatures }} Signatures
            </div>
            <q-linear-progress
              :value="(campaign.signature_count || 0) / campaign.target_signatures"
              color="primary"
              size="12px"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'

export default defineComponent({
  name: 'CampaignDetailPage',
  setup() {
    const route = useRoute()
    const campaign = ref(null)

    onMounted(async () => {
      try {
        const response = await api.get(`/api/campaigns/${route.params.id}`)
        campaign.value = response.data
      } catch (error) {
        console.error(error)
      }
    })

    return { campaign }
  }
})
</script>
