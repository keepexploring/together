<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 1200px; width: 100%">
      <!-- Hero Section -->
      <div class="text-center q-mb-xl">
        <q-icon name="public" size="120px" color="primary" />
        <h1 class="text-h2 text-weight-bold q-mt-md q-mb-md">
          Planet Pledge
        </h1>
        <p class="text-h5 text-grey-7 q-mb-lg">
          Together we can restore and protect our planet
        </p>
        <p class="text-body1 q-mb-xl">
          Make pledges about how you'll reduce your impact on the planet.
          Join with your community, track your progress, and see the collective impact
          when we all work together.
        </p>

        <div class="row q-gutter-md justify-center">
          <q-btn
            size="lg"
            color="primary"
            label="Make a Pledge"
            icon="eco"
            to="/pledge"
            unelevated
          />
          <q-btn
            size="lg"
            color="secondary"
            label="View Impact"
            icon="insights"
            to="/impact"
            outline
          />
          <q-btn
            size="lg"
            color="accent"
            label="Browse Campaigns"
            icon="campaign"
            to="/campaigns"
            outline
          />
        </div>
      </div>

      <!-- Features Section -->
      <div class="row q-col-gutter-lg q-mt-xl">
        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="check_circle" size="64px" color="primary" />
              <h6 class="q-mt-md q-mb-sm">Make Pledges</h6>
              <p class="text-body2">
                Choose from 50+ scientifically-researched environmental actions,
                from everyday choices to creative solutions.
              </p>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="groups" size="64px" color="secondary" />
              <h6 class="q-mt-md q-mb-sm">Join Groups</h6>
              <p class="text-body2">
                Churches, community groups, and organizations can create
                simple codes for members to join and pledge together.
              </p>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="analytics" size="64px" color="accent" />
              <h6 class="q-mt-md q-mb-sm">Track Impact</h6>
              <p class="text-body2">
                See real-time calculations of carbon saved, plastic prevented,
                water conserved, and ecosystems restored.
              </p>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-md-3">
          <q-card flat bordered class="full-height">
            <q-card-section class="text-center">
              <q-icon name="campaign" size="64px" color="positive" />
              <h6 class="q-mt-md q-mb-sm">Launch Campaigns</h6>
              <p class="text-body2">
                Create environmental campaigns on issues you care about
                and gather signatures from the community.
              </p>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Impact Categories -->
      <div class="q-mt-xl">
        <h3 class="text-h4 text-center q-mb-lg">Impact Categories</h3>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="cloud" size="48px" color="primary" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Carbon Reduction</div>
                    <div class="text-caption text-grey-7">
                      Transportation, diet, energy choices
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="recycling" size="48px" color="secondary" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Plastic Reduction</div>
                    <div class="text-caption text-grey-7">
                      Reusables, packaging, lifestyle changes
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="water_drop" size="48px" color="info" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Water Conservation</div>
                    <div class="text-caption text-grey-7">
                      Fixtures, habits, sustainable practices
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="delete" size="48px" color="warning" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Waste Reduction</div>
                    <div class="text-caption text-grey-7">
                      Composting, recycling, repair
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="nature" size="48px" color="positive" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Ecosystem Restoration</div>
                    <div class="text-caption text-grey-7">
                      Tree planting, habitat creation
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 col-lg-4">
            <q-card flat bordered>
              <q-card-section>
                <div class="row items-center">
                  <q-icon name="bolt" size="48px" color="accent" class="q-mr-md" />
                  <div>
                    <div class="text-h6">Energy Conservation</div>
                    <div class="text-caption text-grey-7">
                      Renewables, efficiency, smart choices
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="text-center q-mt-xl q-pa-xl bg-primary text-white" style="border-radius: 8px;">
        <h4 class="text-h4 q-mb-md">Ready to make a difference?</h4>
        <p class="text-body1 q-mb-lg">
          Join thousands of people making pledges to protect our planet
        </p>
        <q-btn
          size="lg"
          color="white"
          text-color="primary"
          label="Get Started"
          to="/pledge"
          unelevated
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'IndexPage'
})
</script>
