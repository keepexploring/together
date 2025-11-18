<template>
  <q-page class="q-pa-md">
    <div style="max-width: 900px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">Organize Your Group</h2>
      <p class="text-body1 q-mb-lg text-grey-7">
        Create a group for your church, community organization, or event.
        Get a simple access code that people can use to join and make pledges together.
      </p>

      <q-card flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">Create Your Organization</div>

          <q-form @submit="createOrganization">
            <q-input
              v-model="form.name"
              label="Organization Name"
              outlined
              required
              class="q-mb-md"
              hint="E.g., 'St. Mary's Church' or 'Green City Initiative'"
            />

            <q-input
              v-model="form.description"
              label="Description"
              type="textarea"
              outlined
              rows="3"
              class="q-mb-md"
              hint="Tell people about your group"
            />

            <q-input
              v-model="form.ownerEmail"
              label="Your Email"
              type="email"
              outlined
              required
              class="q-mb-md"
              hint="You'll be the organizer"
            />

            <q-btn
              type="submit"
              color="primary"
              label="Create Organization"
              icon="add"
              :loading="creating"
              unelevated
              size="lg"
            />
          </q-form>
        </q-card-section>
      </q-card>

      <!-- Success Display -->
      <q-card v-if="createdOrg" flat bordered class="q-mt-lg bg-positive text-white">
        <q-card-section>
          <div class="text-h5 q-mb-md">
            <q-icon name="check_circle" size="32px" class="q-mr-sm" />
            Organization Created!
          </div>

          <div class="q-mb-md">
            <div class="text-subtitle1 text-weight-bold q-mb-xs">Organization Name:</div>
            <div class="text-h6">{{ createdOrg.name }}</div>
          </div>

          <div class="q-mb-md">
            <div class="text-subtitle1 text-weight-bold q-mb-xs">Access Code:</div>
            <div class="text-h4 q-pa-sm" style="background: rgba(255,255,255,0.2); border-radius: 4px; display: inline-block;">
              {{ createdOrg.access_code }}
            </div>
            <q-btn
              flat
              round
              dense
              icon="content_copy"
              @click="copyCode"
              class="q-ml-sm"
            />
          </div>

          <div class="q-mb-md">
            <div class="text-subtitle1 text-weight-bold q-mb-xs">Simple URL:</div>
            <div class="text-body1">
              {{ window.location.origin }}/#/join/{{ createdOrg.access_code }}
            </div>
            <q-btn
              flat
              round
              dense
              icon="content_copy"
              @click="copyUrl"
              class="q-ml-sm"
            />
          </div>

          <div class="q-mt-md">
            <p class="text-body2">
              Share this code or URL with your group members. They can use it to join
              and make pledges that will count toward your organization's collective impact!
            </p>
          </div>
        </q-card-section>
      </q-card>

      <!-- How it Works -->
      <div class="q-mt-xl">
        <h3 class="text-h5 q-mb-md">How It Works</h3>

        <q-timeline color="primary">
          <q-timeline-entry
            title="Create Your Organization"
            subtitle="Step 1"
            icon="add_circle"
          >
            Fill in your organization details and get a unique access code.
          </q-timeline-entry>

          <q-timeline-entry
            title="Share with Your Group"
            subtitle="Step 2"
            icon="share"
          >
            Give the access code to your members via email, social media, or at events.
          </q-timeline-entry>

          <q-timeline-entry
            title="Members Make Pledges"
            subtitle="Step 3"
            icon="eco"
          >
            People use the code to join and make environmental pledges.
          </q-timeline-entry>

          <q-timeline-entry
            title="Track Collective Impact"
            subtitle="Step 4"
            icon="insights"
          >
            See your organization's combined impact on the planet!
          </q-timeline-entry>
        </q-timeline>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'OrganizePage',

  setup() {
    const $q = useQuasar()
    const creating = ref(false)
    const createdOrg = ref(null)

    const form = ref({
      name: '',
      description: '',
      ownerEmail: ''
    })

    const createOrganization = async () => {
      if (!form.value.name || !form.value.ownerEmail) {
        $q.notify({ type: 'warning', message: 'Please fill in required fields' })
        return
      }

      creating.value = true
      try {
        // First create/get user
        await api.post('/api/users/', {
          email: form.value.ownerEmail,
          name: 'Organizer'
        })

        // Then create organization
        const response = await api.post('/api/organizations/', {
          name: form.value.name,
          description: form.value.description
        }, {
          params: { owner_email: form.value.ownerEmail }
        })

        createdOrg.value = response.data

        $q.notify({
          type: 'positive',
          message: 'Organization created successfully!',
          timeout: 3000
        })

        // Reset form
        form.value = { name: '', description: '', ownerEmail: '' }
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: error.response?.data?.detail || 'Failed to create organization'
        })
      } finally {
        creating.value = false
      }
    }

    const copyCode = () => {
      navigator.clipboard.writeText(createdOrg.value.access_code)
      $q.notify({
        type: 'positive',
        message: 'Access code copied!',
        timeout: 1000
      })
    }

    const copyUrl = () => {
      const url = `${window.location.origin}/#/join/${createdOrg.value.access_code}`
      navigator.clipboard.writeText(url)
      $q.notify({
        type: 'positive',
        message: 'URL copied!',
        timeout: 1000
      })
    }

    return {
      form,
      creating,
      createdOrg,
      createOrganization,
      copyCode,
      copyUrl,
      window
    }
  }
})
</script>
