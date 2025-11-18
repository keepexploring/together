<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 600px; width: 100%;">
      <div v-if="organization" class="text-center">
        <q-icon name="groups" size="80px" color="primary" class="q-mb-md" />

        <h2 class="text-h4 q-mb-sm">Join {{ organization.name }}</h2>
        <p class="text-body1 text-grey-7 q-mb-lg">
          {{ organization.description }}
        </p>

        <q-card flat bordered class="q-mb-lg">
          <q-card-section>
            <p class="text-body2">
              You're joining a community of people committed to making a positive
              impact on the planet. Make a pledge below to contribute to
              {{ organization.name }}'s collective impact!
            </p>
          </q-card-section>
        </q-card>

        <q-btn
          size="lg"
          color="primary"
          label="Make a Pledge"
          icon="eco"
          to="/pledge"
          unelevated
        />

        <div class="q-mt-lg text-caption text-grey-6">
          Access Code: {{ code }}
        </div>
      </div>

      <div v-else-if="loading" class="text-center">
        <q-spinner-dots size="50px" color="primary" />
        <p class="text-body1 text-grey-7 q-mt-md">Loading...</p>
      </div>

      <div v-else class="text-center">
        <q-icon name="error" size="80px" color="negative" class="q-mb-md" />
        <h2 class="text-h5 q-mb-md">Invalid Access Code</h2>
        <p class="text-body1 text-grey-7">
          The access code "{{ code }}" is not valid.
        </p>
        <q-btn
          color="primary"
          label="Go Home"
          to="/"
          unelevated
          class="q-mt-md"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'

export default defineComponent({
  name: 'JoinPage',

  setup() {
    const route = useRoute()
    const code = ref(route.params.code)
    const organization = ref(null)
    const loading = ref(true)

    const fetchOrganization = async () => {
      loading.value = true
      try {
        const response = await api.get(`/api/organizations/code/${code.value}`)
        organization.value = response.data
      } catch (error) {
        organization.value = null
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchOrganization()
    })

    return {
      code,
      organization,
      loading
    }
  }
})
</script>
