<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1200px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">Content Management</h2>
      <p class="text-body1 q-mb-lg text-grey-7">
        Manage custom environmental actions for your organization
      </p>

      <q-card flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">Create Custom Action</div>

          <q-form @submit="createAction">
            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="form.title"
                  label="Action Title"
                  outlined
                  required
                />
              </div>

              <div class="col-12 col-md-6">
                <q-select
                  v-model="form.category"
                  :options="categoryOptions"
                  label="Category"
                  outlined
                  required
                  emit-value
                  map-options
                />
              </div>

              <div class="col-12">
                <q-input
                  v-model="form.description"
                  label="Description"
                  type="textarea"
                  outlined
                  required
                  rows="3"
                />
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="form.carbon_saved_kg"
                  label="Carbon Saved (kg CO2)"
                  type="number"
                  outlined
                  step="0.01"
                />
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="form.plastic_saved_kg"
                  label="Plastic Saved (kg)"
                  type="number"
                  outlined
                  step="0.01"
                />
              </div>

              <div class="col-12 col-md-6">
                <q-input
                  v-model.number="form.water_saved_liters"
                  label="Water Saved (liters)"
                  type="number"
                  outlined
                  step="0.01"
                />
              </div>

              <div class="col-12 col-md-6">
                <q-select
                  v-model="form.frequency_type"
                  :options="frequencyOptions"
                  label="Frequency"
                  outlined
                  required
                  emit-value
                  map-options
                />
              </div>

              <div class="col-12">
                <q-input
                  v-model="form.source_info"
                  label="Source/Citation"
                  outlined
                  hint="Where does this impact data come from?"
                />
              </div>

              <div class="col-12">
                <q-btn
                  type="submit"
                  color="primary"
                  label="Create Action"
                  icon="add"
                  :loading="creating"
                  unelevated
                />
              </div>
            </div>
          </q-form>
        </q-card-section>
      </q-card>

      <div class="q-mt-lg text-caption text-grey-6">
        <q-icon name="info" />
        Custom actions are only visible to your organization members.
        For global actions, please contact the platform administrators.
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'CMSPage',

  setup() {
    const $q = useQuasar()
    const creating = ref(false)

    const form = ref({
      title: '',
      description: '',
      category: '',
      carbon_saved_kg: 0,
      plastic_saved_kg: 0,
      water_saved_liters: 0,
      frequency_type: 'yearly',
      source_info: ''
    })

    const categoryOptions = [
      { label: 'Carbon Reduction', value: 'carbon_reduction' },
      { label: 'Plastic Reduction', value: 'plastic_reduction' },
      { label: 'Water Conservation', value: 'water_conservation' },
      { label: 'Waste Reduction', value: 'waste_reduction' },
      { label: 'Ecosystem Restoration', value: 'ecosystem_restoration' },
      { label: 'Energy Conservation', value: 'energy_conservation' }
    ]

    const frequencyOptions = [
      { label: 'Once', value: 'once' },
      { label: 'Daily', value: 'daily' },
      { label: 'Weekly', value: 'weekly' },
      { label: 'Monthly', value: 'monthly' },
      { label: 'Yearly', value: 'yearly' }
    ]

    const createAction = async () => {
      creating.value = true
      try {
        await api.post('/api/actions/', form.value)
        $q.notify({
          type: 'positive',
          message: 'Action created successfully!'
        })
        // Reset form
        form.value = {
          title: '',
          description: '',
          category: '',
          carbon_saved_kg: 0,
          plastic_saved_kg: 0,
          water_saved_liters: 0,
          frequency_type: 'yearly',
          source_info: ''
        }
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to create action'
        })
      } finally {
        creating.value = false
      }
    }

    return {
      form,
      creating,
      categoryOptions,
      frequencyOptions,
      createAction
    }
  }
})
</script>
