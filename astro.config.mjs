// @ts-check
import { defineConfig, sessionDrivers, passthroughImageService } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default defineConfig({
  adapter: cloudflare({
    imageService: 'passthrough'
  }),
  build: {
    assets: 'assets'
  },
  session: {
    driver: sessionDrivers.memory()
  }
});
