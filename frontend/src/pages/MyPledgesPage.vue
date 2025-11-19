<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1200px; margin: 0 auto;">
      <h2 class="text-h3 q-mb-md">My Pledges</h2>
      <p class="text-body1 q-mb-lg text-grey-7">
        Track your environmental commitments and progress
      </p>

      <!-- Filter Tabs -->
      <q-tabs v-model="statusFilter" dense class="q-mb-lg">
        <q-tab name="all" label="All Pledges" />
        <q-tab name="active" label="Active" />
        <q-tab name="completed" label="Completed" />
        <q-tab name="in_progress" label="In Progress" />
      </q-tabs>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
      </div>

      <!-- Pledges List -->
      <div v-else-if="filteredPledges.length > 0">
        <div class="row q-col-gutter-md">
          <div v-for="pledge in filteredPledges" :key="pledge.id" class="col-12">
            <q-card flat bordered class="pledge-card">
              <q-card-section>
                <div class="row items-start q-col-gutter-md">
                  <!-- Main Content -->
                  <div class="col-12 col-md-8">
                    <div class="row items-center q-mb-sm">
                      <div class="col">
                        <div class="text-h6">{{ pledge.action.title }}</div>
                      </div>
                      <div class="col-auto">
                        <q-badge :color="getStatusColor(pledge.status)" class="q-px-md">
                          {{ formatStatus(pledge.status) }}
                        </q-badge>
                      </div>
                    </div>

                    <p class="text-body2 text-grey-7">{{ pledge.action.description }}</p>

                    <!-- Parametric Values -->
                    <div v-if="pledge.action.is_parametric && pledge.parameter_current_value" class="q-mt-sm">
                      <q-chip dense color="blue-1" text-color="primary">
                        <q-icon name="trending_down" class="q-mr-xs" />
                        Reducing from {{ pledge.parameter_current_value }} to {{ pledge.parameter_target_value }}
                        {{ pledge.action.parameter_unit }}
                      </q-chip>
                    </div>

                    <!-- Commitment Text -->
                    <div v-if="pledge.commitment_text" class="q-mt-sm bg-grey-1 q-pa-sm" style="border-radius: 4px;">
                      <div class="text-caption text-weight-bold">My Commitment:</div>
                      <p class="text-body2 q-mb-none">{{ pledge.commitment_text }}</p>
                    </div>

                    <!-- Time Progress Bar -->
                    <div class="q-mt-md">
                      <div class="row items-center q-mb-xs">
                        <div class="col">
                          <span class="text-caption text-weight-bold">Time Progress</span>
                        </div>
                        <div class="col-auto">
                          <span class="text-caption">{{ getTimeRemaining(pledge) }}</span>
                        </div>
                      </div>
                      <q-linear-progress
                        :value="getTimeProgress(pledge)"
                        :color="getProgressColor(pledge)"
                        size="12px"
                        rounded
                      />
                      <div class="text-caption text-grey-6 q-mt-xs">
                        Started {{ formatDate(pledge.start_date) }} •
                        {{ getDaysRemaining(pledge) }} days remaining
                      </div>
                    </div>

                    <!-- Impact Preview -->
                    <div class="q-mt-md">
                      <div class="text-caption text-weight-bold q-mb-xs">Estimated Impact:</div>
                      <div class="row q-gutter-xs">
                        <q-chip v-if="getImpact(pledge, 'carbon') > 0" dense color="green-1" text-color="green-8">
                          <q-icon name="eco" size="xs" class="q-mr-xs" />
                          {{ getImpact(pledge, 'carbon').toFixed(1) }} kg CO₂
                        </q-chip>
                        <q-chip v-if="getImpact(pledge, 'water') > 0" dense color="blue-1" text-color="blue-8">
                          <q-icon name="water_drop" size="xs" class="q-mr-xs" />
                          {{ getImpact(pledge, 'water').toFixed(0) }} L water
                        </q-chip>
                        <q-chip v-if="getImpact(pledge, 'plastic') > 0" dense color="teal-1" text-color="teal-8">
                          <q-icon name="recycling" size="xs" class="q-mr-xs" />
                          {{ getImpact(pledge, 'plastic').toFixed(1) }} kg plastic
                        </q-chip>
                      </div>
                    </div>
                  </div>

                  <!-- Sidebar Actions -->
                  <div class="col-12 col-md-4">
                    <div class="pledge-actions">
                      <!-- Photos -->
                      <div class="q-mb-md">
                        <div class="text-caption text-weight-bold q-mb-xs">Photos</div>
                        <div v-if="pledge.photos && pledge.photos.length > 0" class="photo-grid">
                          <div
                            v-for="photo in pledge.photos"
                            :key="photo.id"
                            class="photo-thumb"
                            @click="viewPhoto(photo)"
                          >
                            <img :src="photo.photo_url" />
                            <div class="photo-overlay">
                              <q-icon name="verified" v-if="photo.verified_by_peers > 0" color="white" size="xs" />
                            </div>
                          </div>
                        </div>
                        <q-btn
                          flat
                          dense
                          color="primary"
                          label="Add Photo"
                          icon="add_a_photo"
                          size="sm"
                          @click="showPhotoUpload(pledge)"
                          class="full-width q-mt-xs"
                        />
                      </div>

                      <!-- Action Buttons -->
                      <div class="action-buttons">
                        <q-btn
                          v-if="pledge.status === 'active' || pledge.status === 'in_progress'"
                          color="positive"
                          label="Mark Complete"
                          icon="check_circle"
                          @click="completePledge(pledge)"
                          unelevated
                          class="full-width q-mb-sm"
                        />
                        <q-btn
                          flat
                          color="grey-7"
                          label="View Details"
                          icon="info"
                          @click="viewPledgeDetails(pledge)"
                          class="full-width"
                        />
                      </div>

                      <!-- Next Follow-up -->
                      <div v-if="pledge.next_follow_up" class="q-mt-md">
                        <q-banner dense rounded class="bg-blue-1">
                          <template v-slot:avatar>
                            <q-icon name="notifications" color="primary" />
                          </template>
                          <div class="text-caption">
                            Next check-in: {{ formatDate(pledge.next_follow_up) }}
                          </div>
                        </q-banner>
                      </div>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <q-card v-else flat bordered class="text-center q-py-xl">
        <q-card-section>
          <q-icon name="eco" size="64px" color="grey-5" />
          <div class="text-h6 q-mt-md text-grey-7">No pledges yet</div>
          <div class="text-body2 text-grey-6 q-mt-sm">
            Make your first pledge to start making a difference!
          </div>
          <q-btn
            color="primary"
            label="Make a Pledge"
            icon="add"
            to="/pledge"
            class="q-mt-md"
            unelevated
          />
        </q-card-section>
      </q-card>

      <!-- Photo Upload Dialog -->
      <q-dialog v-model="showPhotoDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Add Photo Evidence</div>
            <q-space />
            <q-btn flat dense icon="close" v-close-popup />
          </q-card-section>

          <q-form @submit="uploadPhoto">
            <q-card-section>
              <q-input
                v-model="photoForm.photo_url"
                label="Photo URL"
                outlined
                required
                placeholder="https://example.com/photo.jpg"
                class="q-mb-md"
                hint="Upload your photo to an image hosting service and paste the URL"
              />
              <q-input
                v-model="photoForm.caption"
                label="Caption (optional)"
                type="textarea"
                outlined
                rows="3"
                placeholder="Describe your progress..."
              />
            </q-card-section>

            <q-card-actions align="right">
              <q-btn flat label="Cancel" v-close-popup />
              <q-btn
                type="submit"
                color="primary"
                label="Upload Photo"
                :loading="uploading"
                unelevated
              />
            </q-card-actions>
          </q-form>
        </q-card>
      </q-dialog>

      <!-- Photo View Dialog -->
      <q-dialog v-model="showPhotoViewDialog" v-if="selectedPhoto">
        <q-card style="max-width: 800px">
          <q-img :src="selectedPhoto.photo_url" />
          <q-card-section>
            <div class="text-body1">{{ selectedPhoto.caption }}</div>
            <div class="text-caption text-grey-7 q-mt-sm">
              Uploaded {{ formatDate(selectedPhoto.uploaded_at) }}
            </div>
            <div class="q-mt-sm">
              <q-chip color="green" text-color="white">
                <q-icon name="verified" left />
                {{ selectedPhoto.verified_by_peers }} verifications
              </q-chip>
            </div>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Close" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'MyPledgesPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const uploading = ref(false)
    const pledges = ref([])
    const statusFilter = ref('all')
    const showPhotoDialog = ref(false)
    const showPhotoViewDialog = ref(false)
    const selectedPledge = ref(null)
    const selectedPhoto = ref(null)
    const photoForm = ref({
      photo_url: '',
      caption: ''
    })

    // For demo, using user ID 1
    const userId = ref(1)

    const filteredPledges = computed(() => {
      if (statusFilter.value === 'all') return pledges.value
      return pledges.value.filter(p => p.status === statusFilter.value)
    })

    const loadPledges = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/pledges/', {
          params: { user_id: userId.value }
        })
        pledges.value = response.data

        // Load photos for each pledge
        for (const pledge of pledges.value) {
          try {
            const photoResp = await api.get(`/api/pledges/${pledge.id}/photos`)
            pledge.photos = photoResp.data
          } catch (error) {
            pledge.photos = []
          }
        }
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load pledges'
        })
      } finally {
        loading.value = false
      }
    }

    const getStatusColor = (status) => {
      const colors = {
        active: 'positive',
        completed: 'primary',
        in_progress: 'info',
        missed: 'negative'
      }
      return colors[status.toLowerCase()] || 'grey'
    }

    const formatStatus = (status) => {
      return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
    }

    const getTimeProgress = (pledge) => {
      const start = new Date(pledge.start_date)
      const end = new Date(pledge.end_date)
      const now = new Date()
      const total = end - start
      const elapsed = now - start
      return Math.min(Math.max(elapsed / total, 0), 1)
    }

    const getProgressColor = (pledge) => {
      const progress = getTimeProgress(pledge)
      if (progress >= 0.9) return 'positive'
      if (progress >= 0.5) return 'warning'
      return 'info'
    }

    const getTimeRemaining = (pledge) => {
      const days = getDaysRemaining(pledge)
      if (days <= 0) return 'Completed'
      if (days === 1) return '1 day left'
      return `${days} days left`
    }

    const getDaysRemaining = (pledge) => {
      const end = new Date(pledge.end_date)
      const now = new Date()
      const diff = end - now
      return Math.max(Math.ceil(diff / (1000 * 60 * 60 * 24)), 0)
    }

    const getImpact = (pledge, type) => {
      if (pledge.action.is_parametric && pledge.parameter_current_value) {
        const reduction = pledge.parameter_current_value - pledge.parameter_target_value
        if (reduction > 0 && type === 'carbon') {
          const duration_factor = pledge.duration_days / 365.0
          return pledge.action.base_impact_per_unit * reduction * duration_factor
        }
        return 0
      }

      const multiplier = pledge.duration_days / 365.0
      let freqMultiplier = 1
      if (pledge.action.frequency_type === 'daily') freqMultiplier = 365
      else if (pledge.action.frequency_type === 'weekly') freqMultiplier = 52
      else if (pledge.action.frequency_type === 'monthly') freqMultiplier = 12

      const factor = multiplier * freqMultiplier

      if (type === 'carbon') return pledge.action.carbon_saved_kg * factor
      if (type === 'water') return pledge.action.water_saved_liters * factor
      if (type === 'plastic') return pledge.action.plastic_saved_kg * factor
      return 0
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }

    const showPhotoUpload = (pledge) => {
      selectedPledge.value = pledge
      photoForm.value = { photo_url: '', caption: '' }
      showPhotoDialog.value = true
    }

    const uploadPhoto = async () => {
      uploading.value = true
      try {
        await api.post('/api/photos/', {
          pledge_id: selectedPledge.value.id,
          photo_url: photoForm.value.photo_url,
          caption: photoForm.value.caption
        }, {
          params: { user_id: userId.value }
        })

        $q.notify({
          type: 'positive',
          message: 'Photo uploaded successfully!'
        })

        showPhotoDialog.value = false
        await loadPledges() // Reload to show new photo
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to upload photo'
        })
      } finally {
        uploading.value = false
      }
    }

    const viewPhoto = (photo) => {
      selectedPhoto.value = photo
      showPhotoViewDialog.value = true
    }

    const completePledge = async (pledge) => {
      try {
        await api.patch(`/api/pledges/${pledge.id}/status`, null, {
          params: { status_update: 'COMPLETED' }
        })

        $q.notify({
          type: 'positive',
          message: 'Congratulations on completing your pledge!',
          icon: 'celebration'
        })

        await loadPledges()
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to update pledge status'
        })
      }
    }

    const viewPledgeDetails = (pledge) => {
      $q.dialog({
        title: pledge.action.title,
        message: `
          <div>
            <p><strong>Description:</strong> ${pledge.action.description}</p>
            <p><strong>Duration:</strong> ${pledge.duration_days} days</p>
            <p><strong>Status:</strong> ${formatStatus(pledge.status)}</p>
            ${pledge.action.source_info ? `<p><strong>Source:</strong> ${pledge.action.source_info}</p>` : ''}
          </div>
        `,
        html: true
      })
    }

    onMounted(() => {
      loadPledges()
    })

    return {
      loading,
      uploading,
      pledges,
      statusFilter,
      filteredPledges,
      showPhotoDialog,
      showPhotoViewDialog,
      selectedPhoto,
      photoForm,
      getStatusColor,
      formatStatus,
      getTimeProgress,
      getProgressColor,
      getTimeRemaining,
      getDaysRemaining,
      getImpact,
      formatDate,
      showPhotoUpload,
      uploadPhoto,
      viewPhoto,
      completePledge,
      viewPledgeDetails
    }
  }
})
</script>

<style scoped>
.pledge-card {
  transition: box-shadow 0.2s;
}

.pledge-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.pledge-actions {
  display: flex;
  flex-direction: column;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 0.5rem;
}

.photo-thumb {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s;
}

.photo-thumb:hover {
  transform: scale(1.05);
}

.photo-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-overlay {
  position: absolute;
  top: 4px;
  right: 4px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
}
</style>
