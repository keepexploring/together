<template>
  <q-page class="q-pa-md">
    <div style="max-width: 1200px; margin: 0 auto;">
      <div class="row items-center q-mb-lg">
        <div class="col">
          <h2 class="text-h3 q-my-none">Success Stories</h2>
          <p class="text-subtitle1 text-grey-7">
            Inspiring stories from our community members
          </p>
        </div>
        <div class="col-auto">
          <q-btn
            color="primary"
            label="Share Your Story"
            icon="add"
            @click="showSubmitDialog = true"
            unelevated
          />
        </div>
      </div>

      <!-- Filter Tabs -->
      <q-tabs v-model="storyFilter" dense class="q-mb-lg">
        <q-tab name="all" label="All Stories" />
        <q-tab name="featured" label="Featured" />
      </q-tabs>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-py-xl">
        <q-spinner color="primary" size="3em" />
        <div class="text-subtitle1 q-mt-md">Loading stories...</div>
      </div>

      <!-- Stories Grid -->
      <div v-else>
        <div v-if="stories.length > 0" class="row q-col-gutter-md">
          <div
            v-for="story in stories"
            :key="story.id"
            class="col-12 col-md-6 col-lg-4"
          >
            <q-card flat bordered class="story-card full-height">
              <!-- Featured Badge -->
              <q-badge
                v-if="story.is_featured"
                color="amber"
                class="featured-badge"
                floating
              >
                <q-icon name="star" /> Featured
              </q-badge>

              <!-- Story Image -->
              <q-img
                v-if="story.image_url"
                :src="story.image_url"
                ratio="16/9"
                class="story-image"
              >
                <div class="absolute-bottom text-subtitle2 text-center story-image-overlay">
                  {{ story.title }}
                </div>
              </q-img>
              <q-card-section v-else class="bg-gradient text-white text-center">
                <q-icon name="auto_stories" size="64px" />
                <div class="text-h6 q-mt-sm">{{ story.title }}</div>
              </q-card-section>

              <q-card-section>
                <!-- Author Info -->
                <div class="row items-center q-mb-sm">
                  <div class="col-auto">
                    <q-avatar color="primary" text-color="white" size="32px">
                      {{ story.user.name.charAt(0).toUpperCase() }}
                    </q-avatar>
                  </div>
                  <div class="col q-pl-sm">
                    <div class="text-subtitle2">{{ story.user.name }}</div>
                    <div class="text-caption text-grey-7">
                      {{ formatDate(story.submitted_at) }}
                    </div>
                  </div>
                </div>

                <!-- Impact Highlight -->
                <div v-if="story.impact_highlight" class="impact-highlight q-mb-sm">
                  <q-icon name="eco" color="green" />
                  <span class="text-weight-bold">{{ story.impact_highlight }}</span>
                </div>

                <!-- Story Preview -->
                <div class="story-text">
                  {{ getStoryPreview(story.story) }}
                </div>
              </q-card-section>

              <q-card-actions>
                <q-btn
                  flat
                  color="primary"
                  label="Read More"
                  icon-right="arrow_forward"
                  @click="showStoryDetail(story)"
                />
              </q-card-actions>
            </q-card>
          </div>
        </div>

        <!-- Empty State -->
        <q-card v-else flat bordered class="text-center q-py-xl">
          <q-card-section>
            <q-icon name="auto_stories" size="64px" color="grey-5" />
            <div class="text-h6 q-mt-md text-grey-7">No stories yet</div>
            <div class="text-body2 text-grey-6 q-mt-sm">
              Be the first to share your environmental success story!
            </div>
            <q-btn
              color="primary"
              label="Share Your Story"
              icon="add"
              @click="showSubmitDialog = true"
              class="q-mt-md"
              unelevated
            />
          </q-card-section>
        </q-card>
      </div>

      <!-- Submit Story Dialog -->
      <q-dialog v-model="showSubmitDialog" persistent>
        <q-card style="min-width: 600px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Share Your Success Story</div>
            <q-space />
            <q-btn flat dense icon="close" v-close-popup />
          </q-card-section>

          <q-form @submit="submitStory">
            <q-card-section>
              <q-input
                v-model="storyForm.title"
                label="Story Title"
                outlined
                required
                maxlength="100"
                counter
                class="q-mb-md"
              />

              <q-input
                v-model="storyForm.story"
                label="Your Story"
                type="textarea"
                outlined
                required
                rows="8"
                maxlength="2000"
                counter
                hint="Share your journey, challenges overcome, and impact made"
                class="q-mb-md"
              />

              <q-input
                v-model="storyForm.impact_highlight"
                label="Impact Highlight (optional)"
                outlined
                placeholder="e.g., Saved 500kg CO₂ in 6 months"
                class="q-mb-md"
              />

              <q-input
                v-model="storyForm.image_url"
                label="Image URL (optional)"
                outlined
                placeholder="https://..."
                class="q-mb-md"
              />

              <div class="text-caption text-grey-7">
                Your story will be reviewed before being published
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn flat label="Cancel" v-close-popup />
              <q-btn
                type="submit"
                color="primary"
                label="Submit Story"
                :loading="submitting"
                unelevated
              />
            </q-card-actions>
          </q-form>
        </q-card>
      </q-dialog>

      <!-- Story Detail Dialog -->
      <q-dialog v-model="showDetailDialog" v-if="selectedStory">
        <q-card style="max-width: 800px; width: 100%">
          <!-- Story Header -->
          <q-img
            v-if="selectedStory.image_url"
            :src="selectedStory.image_url"
            ratio="21/9"
          />
          <div v-else class="bg-gradient text-white text-center q-pa-xl">
            <q-icon name="auto_stories" size="96px" />
          </div>

          <q-card-section>
            <div class="text-h4 q-mb-md">{{ selectedStory.title }}</div>

            <!-- Author Info -->
            <div class="row items-center q-mb-md">
              <div class="col-auto">
                <q-avatar color="primary" text-color="white" size="48px">
                  {{ selectedStory.user.name.charAt(0).toUpperCase() }}
                </q-avatar>
              </div>
              <div class="col q-pl-md">
                <div class="text-subtitle1">{{ selectedStory.user.name }}</div>
                <div class="text-caption text-grey-7">
                  {{ formatDate(selectedStory.submitted_at) }}
                </div>
              </div>
            </div>

            <!-- Impact Highlight -->
            <q-banner v-if="selectedStory.impact_highlight" rounded class="bg-green-1 q-mb-md">
              <template v-slot:avatar>
                <q-icon name="eco" color="green" />
              </template>
              <div class="text-weight-bold">{{ selectedStory.impact_highlight }}</div>
            </q-banner>

            <!-- Full Story -->
            <div class="text-body1" style="white-space: pre-line;">
              {{ selectedStory.story }}
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              flat
              color="primary"
              label="Inspiring!"
              icon="thumb_up"
              @click="likeStory(selectedStory)"
            />
            <q-btn flat label="Close" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, watch, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'StoriesPage',

  setup() {
    const $q = useQuasar()
    const loading = ref(true)
    const submitting = ref(false)
    const stories = ref([])
    const storyFilter = ref('all')
    const showSubmitDialog = ref(false)
    const showDetailDialog = ref(false)
    const selectedStory = ref(null)

    const storyForm = ref({
      title: '',
      story: '',
      impact_highlight: '',
      image_url: ''
    })

    // For demo purposes, using user ID 1
    const userId = ref(1)

    const loadStories = async () => {
      loading.value = true
      try {
        const params = {
          is_approved: true
        }
        if (storyFilter.value === 'featured') {
          params.is_featured = true
        }

        const response = await api.get('/api/stories/', { params })
        stories.value = response.data
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to load stories'
        })
      } finally {
        loading.value = false
      }
    }

    const submitStory = async () => {
      submitting.value = true
      try {
        await api.post('/api/stories/', storyForm.value, {
          params: { user_id: userId.value }
        })

        $q.notify({
          type: 'positive',
          message: 'Story submitted successfully! It will be reviewed before publishing.',
          timeout: 3000
        })

        // Reset form
        storyForm.value = {
          title: '',
          story: '',
          impact_highlight: '',
          image_url: ''
        }
        showSubmitDialog.value = false
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Failed to submit story'
        })
      } finally {
        submitting.value = false
      }
    }

    const showStoryDetail = (story) => {
      selectedStory.value = story
      showDetailDialog.value = true
    }

    const likeStory = (story) => {
      $q.notify({
        type: 'positive',
        message: 'Thanks for the encouragement!',
        icon: 'thumb_up',
        timeout: 1000
      })
    }

    const getStoryPreview = (text) => {
      const maxLength = 150
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    watch(storyFilter, () => {
      loadStories()
    })

    onMounted(() => {
      loadStories()
    })

    return {
      loading,
      submitting,
      stories,
      storyFilter,
      showSubmitDialog,
      showDetailDialog,
      selectedStory,
      storyForm,
      submitStory,
      showStoryDetail,
      likeStory,
      getStoryPreview,
      formatDate
    }
  }
})
</script>

<style scoped>
.story-card {
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.story-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.story-image {
  cursor: pointer;
}

.story-image-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  padding: 1rem;
}

.featured-badge {
  top: 1rem;
  right: 1rem;
}

.impact-highlight {
  background: #E8F5E9;
  padding: 0.5rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.story-text {
  line-height: 1.6;
  color: #424242;
}

.bg-gradient {
  background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%);
}

.full-height {
  height: 100%;
}
</style>
