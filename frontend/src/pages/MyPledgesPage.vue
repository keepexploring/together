<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1000px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">My Pledges</h2>
      <p class="text-body1 q-mb-lg text-grey-7">
        Track your environmental commitments
      </p>

      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <q-input
            v-model="email"
            label="Enter your email to view your pledges"
            outlined
            type="email"
            @keyup.enter="loadPledges"
          >
            <template v-slot:append>
              <q-btn
                flat
                color="primary"
                label="Load"
                @click="loadPledges"
              />
            </template>
          </q-input>
        </q-card-section>
      </q-card>

      <div v-if="pledges.length > 0">
        <div class="row q-col-gutter-md">
          <div v-for="pledge in pledges" :key="pledge.id" class="col-12">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-start">
                  <div class="col">
                    <div class="text-h6">{{ pledge.action.title }}</div>
                    <q-badge :color="getStatusColor(pledge.status)">
                      {{ pledge.status }}
                    </q-badge>
                  </div>
                  <div class="col-auto">
                    <q-chip color="grey-3" text-color="dark">
                      {{ pledge.duration_days }} days
                    </q-chip>
                  </div>
                </div>
                <p class="text-body2 q-mt-md">{{ pledge.action.description }}</p>
                <div v-if="pledge.commitment_text" class="q-mt-sm">
                  <div class="text-caption text-weight-bold">Your commitment:</div>
                  <p class="text-body2">{{ pledge.commitment_text }}</p>
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
import { defineComponent, ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'MyPledgesPage',
  setup() {
    const $q = useQuasar()
    const email = ref('')
    const pledges = ref([])

    const loadPledges = async () => {
      try {
        const userResp = await api.get(`/api/users/`)
        // This would need proper user lookup by email
        $q.notify({ type: 'info', message: 'Feature coming soon!' })
      } catch (error) {
        $q.notify({ type: 'negative', message: 'Error loading pledges' })
      }
    }

    const getStatusColor = (status) => {
      const colors = {
        active: 'positive',
        completed: 'primary',
        in_progress: 'info',
        missed: 'negative'
      }
      return colors[status] || 'grey'
    }

    return { email, pledges, loadPledges, getStatusColor }
  }
})
</script>
