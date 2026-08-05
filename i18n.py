LANGS = ("en", "ru", "ar")

STR = {
    "en": {
        "welcome_title": "◈  <b>Welcome to RetainX Studio</b>",
        "welcome_body": (
            "  The fastest and most affordable way\n"
            "  to generate AI video, images & audio.\n\n"
            "  ◉  Kling 3.0  ·  Veo 3.1  ·  Sora 2\n"
            "  ◉  Midjourney  ·  Flux  ·  Seedance\n"
            "  ◉  HeyGen  ·  ElevenLabs  ·  LTX\n\n"
            "  Up to <b>3× cheaper</b> than any competitor.\n"
            "  Results delivered in <b>~2 minutes.</b>"
        ),
        "welcome_bonus": "  🎁  <b>{bonus} free coins</b> added to your account.\n  Balance   <b>{coins} coins</b>",
        "what_create": "What would you like to create?",
        "choose_option": "Choose an option:",

        "main_menu_title": "◈  <b>RetainX Studio</b>",
        "main_menu_balance": "  Balance   <b>{coins} coins</b>",
        "main_menu_desc": "  Generate AI video, images & audio\n  at the most competitive rates.",
        "maintenance_banner": "⚠️  <b>Scheduled maintenance: July 10 – 13</b>\n      The bot may be temporarily unavailable.\n",

        "btn_video_generation": "▸  Video Generation",
        "btn_image_generation": "▸  Image Generation",
        "btn_audio_voice": "▸  Audio & Voice",
        "btn_wallet_coins": "◈  Wallet  ·  {coins} coins",
        "btn_pricing": "◎  Pricing",
        "btn_support": "◌  Support",
        "btn_language": "◐  Language",
        "btn_start_generating": "▸  Start Generating",
        "btn_view_pricing": "◎  View Pricing",
        "btn_back": "←  Back",
        "btn_help": "📖  Help",

        # ── Help pages ──
        "help_main_text": (
            "📖  <b>Help — RetainX Studio</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Select a section for detailed info:"
        ),
        "help_start_text": (
            "🚀  <b>Getting Started</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Coin System</b>\n"
            "  1 coin = $0.05   ·   $1 = 20 coins\n"
            "  Minimum top-up: $2 (40 coins)\n\n"
            "  <b>How It Works</b>\n"
            "  1 · Choose a type — Video, Image or Audio\n"
            "  2 · Select a model and parameters\n"
            "  3 · Enter your prompt in any language\n"
            "  4 · Get your result in ~2 minutes\n\n"
            "  <b>Welcome Bonus</b>\n"
            "  20 free coins on first launch 🎁\n\n"
            "  <b>Promo Codes</b>\n"
            "  Use /promo [CODE] to activate\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_video_text": (
            "🎬  <b>Video Generation</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Standard</b>  (available to all)\n"
            "  Seedance 2.0 Fast · Wan 2.7 · LTX 2.3 Pro\n"
            "  Veo 3.1 Lite · Grok 1.5\n\n"
            "  <b>Kling</b>  (available to all)\n"
            "  Kling 3.0 · Kling O3  ·  up to 4K\n\n"
            "  <b>Premium</b>  (Pro / VIP Unlimited)\n"
            "  Veo 3.1 Full · Veo 3.1 Fast · Sora 2 Pro\n\n"
            "  <b>Avatar & Dubbing</b>\n"
            "  HeyGen · ElevenLabs · Lipsync · OmniHuman\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "  Tap a section for details ↓"
        ),
        "help_vid_std_text": (
            "▸  <b>Standard Video Models</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Seedance 2.0 Fast</b>\n"
            "  480p / 720p  ·  4–15 sec\n"
            "  from 5◈ (480p 4s)  to 45◈ (720p 15s)\n\n"
            "<b>Wan 2.7</b>\n"
            "  720p / 1080p  ·  2–15 sec\n"
            "  from 4◈ (720p 2s)  to 45◈ (1080p 15s)\n\n"
            "<b>LTX 2.3 Pro</b>\n"
            "  720p / 1080p / 2K / 4K  ·  6–10 sec\n"
            "  from 6◈ (720p)  to 75◈ (4K 10s)\n\n"
            "<b>Veo 3.1 Lite</b>\n"
            "  720p / 1080p  ·  4–8 sec\n"
            "  from 3◈ (720p 4s)  to 8◈ (1080p 8s)\n\n"
            "<b>Grok 1.5</b>\n"
            "  Up to 15 sec  ·  4◈/sec  (60◈ for 15s)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_prem_text": (
            "★  <b>Premium Video Models</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "  ⚠️ Requires Unlimited Pro / VIP plan\n\n"
            "<b>Veo 3.1 Full</b>  (best Google quality)\n"
            "  720p / 1080p / 4K  ·  4–8 sec\n"
            "  from 15◈ (720p 4s)  to 58◈ (4K 8s)\n\n"
            "<b>Veo 3.1 Fast</b>\n"
            "  720p / 1080p / 4K  ·  4–8 sec\n"
            "  from 8◈ (720p 4s)  to 40◈ (4K 8s)\n\n"
            "<b>Sora 2 Pro</b>  (OpenAI)\n"
            "  720p / 1080p  ·  4–12 sec\n"
            "  from 26◈ (720p 4s)  to 114◈ (1080p 12s)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_kling_text": (
            "◉  <b>Kling Video Models</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Kling 3.0</b>\n"
            "  720p / 1080p / 4K  ·  3–15 sec\n"
            "  from 4◈ (720p 3s)  to 75◈ (4K 15s)\n\n"
            "<b>Kling O3</b>  (ultra quality)\n"
            "  720p / 1080p / 4K  ·  3–15 sec\n"
            "  from 4◈ (720p 3s)  to 75◈ (4K 15s)\n\n"
            "  ✓ Precise prompt adherence\n"
            "  ✓ Photorealistic scenes\n"
            "  ✓ Reference image support\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_avatar_text": (
            "◌  <b>Avatar & Dubbing</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>HeyGen Avatar</b>\n"
            "  720p / 1080p  ·  1–15 min  ·  60◈/min\n\n"
            "<b>ElevenLabs Dubbing</b>\n"
            "  Professional AI dubbing  ·  60◈/min\n"
            "  29 languages supported\n\n"
            "<b>Lipsync</b>\n"
            "  Lip sync to custom audio  ·  60◈/min\n\n"
            "<b>OmniHuman / Aurora Avatar</b>\n"
            "  Avatar from photo + voice\n"
            "  60◈/min (OmniHuman)  ·  54◈/min (Aurora)\n\n"
            "  Formats: MP4, MOV, AVI\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_images_text": (
            "🖼  <b>Image Generation</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Nano Banana Pro</b>   1K–2K: 3◈  ·  4K: 4◈\n"
            "  <b>Nano Banana 2</b>     1K–2K: 2◈  ·  4K: 3◈\n"
            "  <b>Seedream 5.0 Pro</b>  1K: 1◈  ·  2K: 2◈\n"
            "  <b>GPT Image 2</b>       1K: 1◈  ·  2K: 2◈  ·  4K: 3◈\n"
            "  <b>Wan 2.7 Pro</b>       4K: 2◈\n"
            "  <b>Flux 2.0 Pro</b>      1K–2K: 1◈\n"
            "  <b>Ideogram v3</b>       Turbo/Balanced: 1◈  ·  Quality: 2◈\n"
            "  <b>Topaz Upscaler</b>    2K: 2◈  ·  4K: 3◈  ·  8K: 6◈\n\n"
            "  Formats: 1:1 · 16:9 · 9:16 · 3:4 and more\n"
            "  Reference images: up to 14 per generation\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_audio_text": (
            "🔊  <b>Audio & Voice</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>ElevenLabs Voiceover</b>\n"
            "  Professional AI text-to-speech\n\n"
            "  ✓ 1000+ voices\n"
            "  ✓ Emotion and speech style control\n"
            "  ✓ Voice stability adjustment\n"
            "  ✓ Audio effects processing\n"
            "  ✓ Speech speed control\n"
            "  ✓ 30+ languages\n\n"
            "  Available with Unlimited Pro / VIP plan\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_text": (
            "◈  <b>Wallet & Payment</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Your balance is stored in RetainX coins.\n"
            "  Coins are deducted automatically\n"
            "  on each generation.\n\n"
            "  Select a section for details:"
        ),
        "help_wallet_rates_text": (
            "◎  <b>Rates & Limits</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Coin Rate</b>\n"
            "  1 coin = $0.05\n"
            "  $1 = 20 coins\n\n"
            "  <b>Top-Up Limits</b>\n"
            "  Minimum:      $2.00 = 40 coins\n"
            "  Via Stars:    min. 40 coins\n"
            "  Via USDT:     min. $2\n\n"
            "  <b>Payment Methods</b>\n"
            "  ⭐ Telegram Stars\n"
            "  ₮ USDT (TRC-20)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_stars_text": (
            "⭐  <b>Top Up via Telegram Stars</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>How to top up:</b>\n"
            "  1 · Tap «◈ Wallet» in the main menu\n"
            "  2 · Tap «＋ Add Coins»\n"
            "  3 · Choose «⭐ Stars»\n"
            "  4 · Enter the coin amount (min. 40)\n"
            "  5 · Pay via Telegram — no app switch needed\n\n"
            "  Stars → coins rate is calculated automatically.\n\n"
            "  ✓ Instant credit\n"
            "  ✓ No card or crypto wallet required\n"
            "  ✓ Secure — built into Telegram\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_usdt_text": (
            "₮  <b>Top Up via USDT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Network: TRC-20 (Tron)\n\n"
            "  <b>How to top up:</b>\n"
            "  1 · Tap «◈ Wallet» → «＋ Add Coins»\n"
            "  2 · Choose «₮ USDT»\n"
            "  3 · Enter amount in USD (min. $2)\n"
            "  4 · Send USDT to the displayed address\n"
            "  5 · Notify the operator about your payment\n\n"
            "  ✓ USDT TRC-20 accepted\n"
            "  ✓ Credit within 15 minutes\n"
            "  ✓ No bot-side commission\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_text": (
            "⚡  <b>Unlimited Plans</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  An Unlimited plan removes all restrictions\n"
            "  and unlocks additional models.\n\n"
            "  Active for 1, 2, or 3 hours — generate\n"
            "  as many times as you want during that time.\n\n"
            "  <b>Plans:</b>\n"
            "  ⚡  Standard  —  from 268◈/hr\n"
            "  ⚡⚡  Pro       —  from 662◈/hr\n"
            "  ♛   VIP       —  from 1619◈/hr\n\n"
            "  Tap a plan for details ↓\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_std_text": (
            "⚡  <b>Unlimited Standard</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Prices:</b>\n"
            "  1 hr  —  268◈\n"
            "  2 hr  —  482◈  (save 10%)\n"
            "  3 hr  —  642◈  (save 20%)\n\n"
            "  <b>Available Models:</b>\n"
            "  ✓ Seedance 2.0 Fast  ·  Wan 2.7\n"
            "  ✓ LTX 2.3 Pro  ·  Veo 3.1 Lite\n"
            "  ✓ Grok 1.5\n"
            "  ✓ Kling 3.0  ·  Kling O3\n\n"
            "  <b>Max Resolution:</b>  720p\n\n"
            "  ✕ Premium models (Veo Full, Sora)\n"
            "  ✕ Avatar & Dubbing\n"
            "  ✕ Audio generation\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_pro_text": (
            "⚡⚡  <b>Unlimited Pro</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Prices:</b>\n"
            "  1 hr  —  662◈\n"
            "  2 hr  —  1192◈  (save 10%)\n"
            "  3 hr  —  1589◈  (save 20%)\n\n"
            "  <b>Available Models:</b>\n"
            "  ✓ All Standard models\n"
            "  ✓ Veo 3.1 Full  ·  Veo 3.1 Fast\n"
            "  ✓ Sora 2 Pro\n"
            "  ✓ Kling 3.0  ·  Kling O3\n"
            "  ✓ ElevenLabs Voiceover (audio)\n\n"
            "  <b>Max Resolution:</b>  1080p\n\n"
            "  ✕ Avatar & Dubbing\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_vip_text": (
            "♛  <b>Unlimited VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Prices:</b>\n"
            "  1 hr  —  1619◈\n"
            "  2 hr  —  2914◈  (save 10%)\n"
            "  3 hr  —  3886◈  (save 20%)\n\n"
            "  <b>Available Models:</b>\n"
            "  ✓ All Standard and Pro models\n"
            "  ✓ Veo 3.1 Full  ·  Sora 2 Pro\n"
            "  ✓ Kling 3.0  ·  Kling O3\n"
            "  ✓ ElevenLabs Voiceover (audio)\n\n"
            "  <b>Max Resolution:</b>  4K\n\n"
            "  ✓ Full access to all features\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_ref_text": (
            "👥  <b>Referral Program</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Share your link → friend registers and tops up\n"
            "  → you earn % of every top-up they make.\n\n"
            "  <b>Reward Tiers:</b>\n"
            "  Starter (0–5 referrals)\n"
            "    First top-up  20%  ·  Repeat  10%\n\n"
            "  Partner (6–15 referrals)\n"
            "    First top-up  22%  ·  Repeat  12%\n\n"
            "  Pro (16+ referrals)\n"
            "    First top-up  25%  ·  Repeat  15%\n\n"
            "  <b>Blogger Promo Codes</b>\n"
            "  Works like a referral link.\n"
            "  New users enter /promo CODE to activate.\n\n"
            "  Your link: ◈ Wallet → Referral Program\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_support_text": (
            "💬  <b>Support</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Have a question or issue?\n"
            "  Write to us directly:\n\n"
            "  @RetainXStudio\n\n"
            "  <b>Response time:</b>  usually within 1 hour\n\n"
            "  <b>We can help with:</b>\n"
            "  ✓ Video / image not received\n"
            "  ✓ Incorrect coin deduction\n"
            "  ✓ Top-up problems\n"
            "  ✓ Technical errors\n"
            "  ✓ Questions about models\n\n"
            "  For promo codes and partnerships —\n"
            "  also contact @RetainXStudio\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        # ── Help button labels ──
        "help_btn_start":       "🚀  Getting Started",
        "help_btn_video":       "🎬  Video Generation",
        "help_btn_vid_std":     "▸  Standard Models",
        "help_btn_vid_prem":    "★  Premium Models",
        "help_btn_vid_kling":   "◉  Kling",
        "help_btn_vid_avatar":  "◌  Avatar & Dubbing",
        "help_btn_images":      "🖼  Image Generation",
        "help_btn_audio":       "🔊  Audio & Voice",
        "help_btn_wallet":      "◈  Wallet & Payment",
        "help_btn_wallet_rates":"◎  Rates & Limits",
        "help_btn_wallet_stars":"⭐  Telegram Stars",
        "help_btn_wallet_usdt": "₮  USDT / Crypto",
        "help_btn_unlim":       "⚡  Unlimited Plans",
        "help_btn_unlim_std":   "⚡  Standard",
        "help_btn_unlim_pro":   "⚡⚡  Pro",
        "help_btn_unlim_vip":   "♛  VIP",
        "help_btn_ref":         "👥  Referral Program",
        "help_btn_support":     "💬  Support",

        "audio_title": "◌  <b>Audio & Voice</b>",
        "audio_body": "  Coming soon.\n\n  We are integrating voice synthesis\n  and music generation tools.\n\n  Stay tuned.",
        "audio_pro_vip_body": "  Audio & Voice is available on\n  <b>Pro</b> and <b>VIP</b> unlimited plans.\n\n  Upgrade your plan to access\n  voice synthesis and audio generation.",
        "audio_unlimited_only": "  Voice generation is available as part of the\n  <b>Unlimited subscription</b>.\n\n  Subscribe to an Unlimited plan to unlock\n  AI voiceovers with full voice catalog access.",

        "tts_coin_menu_body":   "  Generate AI voiceovers using your coins.\n  Choose a TTS model:",
        "tts_select_voice":     "Select a voice:",
        "tts_page_indicator":   "Page {page}/{total}",
        "tts_voice_card_prompt":"  Listen to a preview, then choose this voice.",
        "tts_btn_preview":      "🎵  Preview",
        "tts_btn_choose":       "✓  Choose This Voice",
        "tts_enter_text_prompt":"  Enter the text to convert to speech.\n  Max {max} characters.",
        "tts_text_too_long":    "  Text is too long (max {max} characters).\n  Please shorten it and try again.",
        "tts_order_summary_title": "◈  <b>Order Summary</b>",
        "tts_voice_label":      "  Voice:    <b>{name}</b>",
        "tts_model_label":      "  Model:    {model}",
        "tts_cost_label":       "  Cost:     ",
        "tts_balance_label":    "  Balance:  ",
        "tts_text_label":       "  Text:",
        "tts_confirm_btn":      "Generate ({coins}◈)",
        "tts_edit_text_btn":    "Edit Text",
        "tts_order_placed_title": "◈  <b>Order #{oid} Placed</b>",
        "tts_voice_row":        "  Voice     <b>{name}</b>",
        "tts_coins_deducted":   "  {coins}◈ deducted from your balance",
        "tts_estimated_delivery":"  Estimated: ~{minutes} min",
        "tts_will_deliver":     "  Audio will be sent here when ready.",
        "tts_session_expired":  "Session expired, please start over.",
        "tts_insufficient_coins":"Insufficient coins. Please top up your balance.",

        "vid_subcat_tier_alert": "This category is not included in your current plan.",

        "vo_low_balance_notice": "Low balance: {coins} coins — top up before ordering.",
        "vo_select_model": "  Select a voice AI model:",
        "vo_select_category": "  Select a voice category:",
        "vo_select_gender": "  Select a voice gender:",
        "vo_select_age": "  Select a voice age:",
        "vo_select_voice": "  Select a voice:",
        "vo_btn_listen_all": "🔊  Listen to all ({count})",
        "vo_listen_all_sending": "🔊 Sending previews…",
        "vo_select_language": "  Select a language:",
        "vo_preview_error": "⚠️  Preview failed. Please try again.",
        "vo_voice_gender_label": "  Gender    {gender}",
        "vo_voice_age_label": "  Age          {age}",
        "vo_voice_category_label": "  Category   {category}",
        "vo_voice_model_label": "  Model       {model}",
        "vo_voice_language_label": "  Language   {language}",
        "vo_btn_choose_voice": "✓  Use this voice",
        "vo_btn_listen": "🎧  Listen to sample",
        "vo_btn_change_language": "🌐  Change language  ·  {language}",
        "vo_preview_caption": "🎧  {voice}  —  {language}  ({model})",
        "vo_voice_stability_label": "  Stability   {pct}%",
        "vo_voice_effect_label": "  Effect       {effect}",
        "vo_btn_stability": "🎚  Stability  ·  {pct}%",
        "vo_select_stability": "  Adjust voice stability.\n  Lower is more expressive, higher is more consistent.",
        "vo_btn_effect": "🎭  Effect  ·  {effect}",
        "vo_select_effect": "  Select a voice effect:",
        "vo_effect_preview_caption": "🎭  {effect}  —  effect preview",
        "vo_btn_done": "✓  Done",
        "vo_stability_label": "  Stability     <b>{pct}%</b>",
        "vo_effect_label": "  Effect         <b>{effect}</b>",
        "vo_voice_emotion_label": "  Emotion     {emotion}",
        "vo_btn_emotion": "🙂  Emotion  ·  {emotion}",
        "vo_select_emotion": "  Select an emotion:",
        "vo_emotion_label": "  Emotion       <b>{emotion}</b>",
        "vo_voice_speed_label": "  Speed         {speed}x",
        "vo_btn_speed": "⏱  Speed  ·  {speed}x",
        "vo_select_speed": "  Adjust speech speed.",
        "vo_speed_label": "  Speed          <b>{speed}x</b>",
        "vo_enter_text": "  Enter the text you want this voice to say:",
        "vo_edit_text_prompt": "  Enter the new text for this voice:",
        "vo_order_summary_title": "◈  <b>Voiceover Order Summary</b>",
        "vo_voice_label": "  Voice          <b>{name}</b>",
        "vo_model_label": "  Model         <b>{model}</b>",
        "vo_language_label": "  Language     <b>{language}</b>",
        "vo_text_label": "  Text",
        "vo_cost_label": "  Cost           ",
        "vo_balance_label": "  Balance      ",
        "vo_btn_confirm": "✓  Confirm  ·  {coins} coins",
        "vo_btn_edit_text": "✎  Edit text",
        "vo_session_expired": "Session expired, please start over.",
        "vo_insufficient_coins": "Insufficient coins. Please top up your wallet.",
        "vo_order_placed_title": "✓  <b>Voiceover order #{oid} placed!</b>",
        "vo_voice_row": "  Voice          <b>{name}</b>",
        "vo_coins_deducted": "  Coins deducted   <b>{coins} coins</b>",
        "vo_estimated_delivery": "  Estimated delivery: ~{minutes} min",
        "vo_will_deliver": "  We will deliver your audio file right here in this chat.",

        "support_title": "◌  <b>Support</b>",
        "support_body": "  Contact us: @RetainXStudio",

        "video_title": "◈  <b>Video Generation</b>",
        "select_category": "Select a category:",

        "images_title": "◈  <b>Image Generation</b>",
        "select_model": "Select a model:",

        "pricing_title": "◎  <b>Pricing</b>",
        "pricing_body": "  1 coin  =  <b>$0.05</b>\n\n  Select a category to view rates:",
        "btn_image_pricing": "▸  Image Pricing",
        "btn_video_pricing": "▸  Video Pricing",

        "price_images_title": "◎  <b>Image Pricing</b>",
        "price_video_title": "◎  <b>Video Pricing</b>",
        "price_video_body": (
            "  Prices vary by model, resolution & duration.\n"
            "  Select a model in Video Generation\n"
            "  to see exact coin costs per option.\n\n"
            "  <b>Sample rates:</b>\n"
            "  Kling 3.0   720p  5s  —  6◈\n"
            "  Veo 3.1     4K    8s  —  58◈\n"
            "  Seedance   1080p 10s  —  60◈\n"
        ),

        "menu_main_menu": "⌂  Main Menu",
        "menu_wallet": "◈  Wallet",
        "menu_video": "▸  Video",
        "menu_images": "▸  Images",
        "menu_audio": "▸  Audio",
        "menu_orders": "≡  Orders",
        "menu_support": "◌  Support",

        "lang_title": "◐  <b>Language</b>",
        "lang_desc": "  Choose your preferred language:",
        "lang_changed": "✓  Language updated.",

        "coins_word": "coins",

        # ── Image generation flow ──────────────────────────────
        "img_menu_title": "◈  <b>Image Generation</b>",
        "img_menu_select": "Select a model to continue:",
        "img_price_label": "Price",
        "img_per_gen": "per generation",
        "img_select_ar": "Select aspect ratio:",
        "img_select_quality": "Select quality:",
        "img_aspect_ratio_label": "Aspect ratio",
        "img_quality_label": "Quality",
        "img_cost_label": "Cost",
        "img_balance_label": "Your balance",
        "img_attach_optional": "  Attach reference images (optional)\n  or skip to write your prompt.",
        "img_btn_add_ref": "◈  Add Image Reference  (up to {max})",
        "img_btn_skip_prompt": "▸  Skip — Write Prompt",
        "img_enter_prompt": "Enter your prompt:",
        "img_order_summary_title": "◈  <b>Order Summary</b>",
        "img_model_label": "Model",
        "img_prompt_label": "Prompt:",
        "img_btn_confirm": "◈  Confirm  ({coins} coins)",
        "img_btn_confirm_free": "◈  Confirm  (free)",
        "img_btn_edit_prompt": "✎  Edit Prompt",
        "img_edit_prompt_prompt": "✎  Enter your new prompt:",
        "img_session_expired": "Session expired. Please start your order again.",
        "img_insufficient_coins": "Insufficient coins. Please top up your wallet.",
        "img_order_error": "⚠️  Failed to place order. Your coins have been refunded.",
        "img_order_placed_title": "◌  <b>Order #{oid} Placed</b>",
        "img_model_row": "  Model     <b>{name}</b>",
        "img_coins_deducted": "  Coins      <b>{coins} deducted</b>",
        "img_estimated_time": "  Estimated time  ~{minutes} min",
        "img_will_deliver": "  We will deliver your image here shortly.",
        "img_ref_title": "◈  <b>Image Reference</b>  ({count}/{max})",
        "img_ref_instructions": (
            "  Send up to <b>{max} images</b> as reference.\n\n"
            "  <code>@img1</code>, <code>@img2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each image\n"
            "  in words in your prompt instead.\n\n"
            "  Tap <b>Done</b> when finished."
        ),
        "btn_done": "✓  Done",
        "img_ref_saved": "✓  Image @img{n} saved.  ({count}/{max})",
        "img_ref_send_more": "Send more or tap Done.",
        "img_ref_max_reached": "Maximum reached. Tap Done.",
        "img_ref_max_alert": "Maximum {max} images reached. Tap Done to continue.",
        "img_ref_required_alert": "Please attach an image before continuing.",
        "img_refs_attached": "  ◈  {count} image ref(s) attached\n",

        # ── Video generation flow ──────────────────────────────
        "vid_menu_title": "◈  <b>Video Generation</b>",
        "vid_select_category": "Select a category:",
        "vid_low_balance_notice": "Low balance: {coins} coins — top up before ordering.",
        "vid_sub_standard": "▸  Standard Video",
        "vid_sub_grok": "▸  Grok Video",
        "vid_sub_premium": "▸  Premium Video",
        "vid_sub_kling": "▸  Kling Video",
        "vid_sub_avatar": "▸  Avatar & Dubbing",
        "vid_select_model": "Select a model:",
        "vid_unknown_tool": "Tool not found",
        "vid_resolution_word": "Resolution",
        "vid_duration_word": "Duration",
        "vid_sec_word": "sec",
        "vid_type_word": "Type",
        "vid_avatar_video_word": "Avatar Video",
        "vid_select_resolution": "  Select resolution:",
        "vid_select_aspect_ratio": "  Select aspect ratio:",
        "vid_select_duration": "  Select duration:",
        "vid_resolution_label": "  Resolution    {res}",
        "vid_aspect_ratio_label": "  Aspect ratio  {ar}",
        "vid_duration_label": "  Duration       {dur} sec",
        "vid_cost_label": "  Cost              <b>{coins} coins</b>",
        "vid_cost_label_short": "  Cost   <b>{coins} coins</b>",
        "vid_balance_label": "  Balance        {coins} coins",
        "vid_audio_label": "  Audio            {audio}",
        "vid_audio_yes": "Yes",
        "vid_audio_no": "No",
        "vid_include_audio": "  Include audio in the video?",
        "vid_btn_with_audio": "🔊  With Audio",
        "vid_btn_no_audio": "🔇  No Audio",
        "vid_enter_prompt": "Enter your prompt:",
        "vid_btn_confirm": "◈  Confirm  ({coins} coins)",
        "vid_btn_edit_prompt": "✎  Edit Prompt",
        "vid_edit_prompt_prompt": "✎  Enter your new prompt:",
        "vid_order_summary_title": "◈  <b>Order Summary</b>",
        "vid_model_label": "  Model          <b>{name}</b>",
        "vid_language_label": "  Language      {lang}",
        "vid_attachments_label": "\n  Attachments:\n",
        "vid_prompt_label": "  Prompt:",
        "vid_session_expired": "Session expired. Please start your order again.",
        "vid_insufficient_coins": "Insufficient coins. Please top up your wallet.",
        "vid_avatar_blocked_unlimited": "Avatar tools are not available during the Unlimited pass.",
        "vid_order_error": "⚠️  Failed to place order. Your coins have been refunded.",
        "vid_order_placed_title": "◌  <b>Order #{oid} Placed</b>",
        "vid_model_row": "  Model     <b>{name}</b>",
        "vid_coins_deducted": "  Coins      <b>{coins} deducted</b>",
        "vid_estimated_delivery": "  Estimated delivery  ~{minutes} min",
        "vid_will_deliver": "  Your result will be sent here.",
        "order_ready_caption": (
            "◈  <b>Your Order is Ready</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Order     #{oid}\n"
            "  Model     {tool}\n\n"
            "  Thank you for choosing RetainX Studio."
        ),

        "vid_grok_title": "◈  <b>Grok Imagine 1.5</b>",
        "vid_grok_resolution_line": "  Resolution: 720p\n\n  Select duration:",
        "vid_grok_res_select": "  Resolution: {res}\n\n  Select duration:",
        "vid_grokt_title": "◈  <b>Grok Text-to-Video</b>",
        "vid_groki_title": "◈  <b>Grok Image-to-Video</b>",
        "vid_btn_char_photo":   "Character Photo",
        "vid_char_photo_title": "◈  <b>Character Photo</b>",
        "vid_char_photo_desc":  "  Send a photo of the character you want to animate.\n\n  The model will generate movement inspired by this photo.",
        "vid_grok_mode_select": "  Select generation mode:",
        "vid_grok_mode_fun": "Fun",
        "vid_grok_mode_normal": "Normal",
        "vid_grok_mode_spicy": "Spicy",
        "vid_grok_extend_prompt": "◈  <b>Grok Extend  +{secs}s</b>\n━━━━━━━━━━━━━━━━━━━━\n\n  Enter a prompt to guide the extension (optional):",
        "vid_grok_task_expired": "This video's task has expired and can no longer be extended or upscaled. Please generate a new video.",

        "vid_grokimag_title":  "◈  <b>Grok Imagine</b>",
        "vid_grokimag_select": "  Select a generation type:",
        "vid_grokimag_15":    "Grok Imagine 1.5  —  Classic",
        "vid_grokimag_t2v":   "Text-to-Video",
        "vid_grokimag_i2v":   "Image-to-Video",

        "vid_extend_title": "◈  <b>Veo 3.1 — Extend Video</b>",
        "vid_extend_desc": "  Extend your video with additional seconds.\n\n  Select the extension tier:",
        "vid_extend_fast":    "⚡  Fast",
        "vid_extend_premium": "◈  Premium",

        "vid_unknown_tool_alert": "Unknown tool",
        "vid_select_lang_label": "◈  Select target language:",
        "vid_translate_cost": "  Cost   <b>{coins} coins</b>",
        "vid_send_video_any_format": "  Send your video file in any format\n  (MP4, MOV, AVI, MKV etc.)",
        "vid_please_send_video": "Please send a video file (MP4, MOV, AVI, MKV etc.)\n\nType /cancel to exit.",
        "vid_video_received": "✓  Video received",
        "vid_add_notes_prompt": "  Add any additional notes (optional)\n  or skip to confirm order:",
        "vid_btn_add_notes": "✎  Add Notes",
        "vid_add_notes_only": "✎  Add notes or instructions (optional):",

        "vid_attach_start_frame": "  ◈  Start frame\n",
        "vid_attach_end_frame": "  ◈  End frame\n",
        "vid_attach_imgs": "  ◈  {count} image ref(s)\n",
        "vid_attach_vids": "  ◈  {count} video ref(s)\n",
        "vid_attach_auds": "  ◈  {count} audio file(s)\n",

        "vid_attach_optional_inline": "Attach reference files (optional)\n  or skip directly to your prompt.",
        "vid_sd_attach_warning": (
            "  ⚠️  Start/End Frame cannot be combined\n"
            "  with other attachment types."
        ),
        "vid_btn_start_frame": "Start Frame",
        "vid_btn_end_frame": "End Frame",
        "vid_btn_clear_startend": "✕  Clear Start/End",
        "vid_btn_clear": "✕  Clear",
        "vid_btn_image_ref": "◈  Image Ref  ({count}/{max})",
        "vid_btn_image_reference": "◈  Image Reference",
        "vid_btn_image_reference_max": "◈  Image Reference  (up to {max})",
        "vid_btn_video_ref": "◈  Video Ref  ({count}/{max})",
        "vid_btn_video_reference": "◈  Video Reference",
        "vid_btn_video_reference_max": "◈  Video Reference  (up to {max}){req}",
        "vid_btn_audio_file": "◈  Audio File  ({count}/{max})",
        "vid_btn_audio_file_plain": "◈  Audio File",
        "vid_btn_audio_file_max": "◈  Audio File  (up to {max})",
        "vid_btn_start_end_frame": "◈  Start & End Frame",
        "vid_btn_start_frame_only": "◈  Start Frame",
        "vid_required_label": " *required",
        "vid_btn_write_prompt": "✓  Write Prompt →",
        "vid_btn_skip_write_prompt": "▸  Skip — Write Prompt",
        "vid_btn_confirm_order": "◈  Confirm Order",
        "vid_btn_upload_required": "⚠️  Upload {items} to continue",
        "vid_required_and": " & ",
        "vid_required_video": "video",
        "vid_required_image": "image",
        "vid_required_audio": "audio",
        "vid_required_start_frame": "start frame",
        "vid_required_files_alert": "Please upload required files: {items}",
        "vid_required_files_alert_simple": "Please upload the required files first.",

        "vid_start_frame_title": "◈  <b>Start Frame</b>",
        "vid_start_frame_desc": "  Send the image for the <b>first frame</b> of your video.\n\n  Reference it in your prompt as <code>@start</code>",
        "vid_start_frame_desc_short": "  Send the image for the <b>first frame</b>.\n\n  Reference it in your prompt as <code>@start</code>",
        "vid_end_frame_title": "◈  <b>End Frame</b>",
        "vid_end_frame_desc": "  Send the image for the <b>last frame</b> of your video.\n\n  Reference it in your prompt as <code>@end</code>",
        "vid_end_frame_desc_short": "  Send the image for the <b>last frame</b>.\n\n  Reference it in your prompt as <code>@end</code>",
        "vid_please_send_image": "◈  Please send an image file (JPG, PNG, WEBP etc.)",
        "vid_please_send_video_short": "◈  Please send a video file (MP4, MOV, AVI etc.)",
        "vid_please_send_audio": "◈  Please send an audio file (MP3, OGG, WAV, M4A etc.)",
        "err_file_too_large": "⚠️  This file is too large — Telegram bots can only download files up to 20MB. Please compress it or send a smaller file.",
        "vid_start_frame_saved": "✓  Start frame saved.\n\nNow set the End Frame or write your prompt.",
        "vid_end_frame_saved": "✓  End frame saved.\n\nWrite your prompt when ready.",

        "vid_img_ref_title": "◈  <b>Image Reference</b>  ({count}/{max})",
        "vid_img_ref_instructions": (
            "  Send up to <b>{max} images</b> as reference.\n\n"
            "  <code>@img1</code>, <code>@img2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each image\n"
            "  in words in your prompt instead (e.g. \"the woman in photo 1\").\n\n"
            "  Send images one by one or as album.\n"
            "  Tap <b>Done</b> when finished."
        ),
        "vid_img_ref_instructions_short": (
            "  Send up to <b>{max} image(s)</b>.\n"
            "  <code>@img1</code> etc. are just labels for you — the AI\n"
            "  doesn't read them. Describe each image in words instead.\n\n"
            "  Tap Done when finished."
        ),
        "vid_img_max_reached": "Maximum {max} images reached. Tap Done to continue.",
        "vid_img_max_reached_short": "Maximum {max} image(s) reached. Tap Done.",
        "vid_img_saved": "✓  Image @img{n} saved.  ({count}/{max})",
        "vid_img_saved_short": "✓  @img{n} saved  ({count}/{max})",
        "vid_send_more_or_done": "Send more or tap Done.",
        "vid_max_reached_tap_done": "Maximum reached. Tap Done.",

        "vid_vid_ref_title": "◈  <b>Video Reference</b>  ({count}/{max})",
        "vid_vid_ref_instructions": (
            "  Send up to <b>{max} videos</b> as reference.\n\n"
            "  <code>@vid1</code>, <code>@vid2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each video\n"
            "  in words in your prompt instead.\n\n"
            "  Tap <b>Done</b> when finished."
        ),
        "vid_vid_ref_instructions_short": (
            "  Send up to <b>{max} video(s)</b> in any format.\n"
            "  <code>@vid1</code> etc. are just labels for you — the AI\n"
            "  doesn't read them. Describe each video in words instead.\n\n"
            "  Tap Done when finished."
        ),
        "vid_vid_max_reached": "Maximum {max} videos reached. Tap Done to continue.",
        "vid_vid_max_reached_short": "Maximum {max} video(s) reached. Tap Done.",
        "vid_vid_saved": "✓  Video @vid{n} saved.  ({count}/{max})",
        "vid_vid_saved_short": "✓  @vid{n} saved  ({count}/{max})",

        "vid_aud_ref_title": "◈  <b>Audio File</b>  ({count}/{max})",
        "vid_aud_ref_instructions": (
            "  Send up to <b>{max} audio files</b>.\n\n"
            "  <code>@aud1</code>, <code>@aud2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each audio\n"
            "  file in words in your prompt instead.\n\n"
            "  Tap <b>Done</b> when finished."
        ),
        "vid_aud_ref_instructions_short": (
            "  Send up to <b>{max} audio file(s)</b>.\n"
            "  <code>@aud1</code> etc. are just labels for you — the AI\n"
            "  doesn't read them. Describe each audio file in words instead.\n\n"
            "  Tap Done when finished."
        ),
        "vid_aud_max_reached": "Maximum {max} audio files reached. Tap Done to continue.",
        "vid_aud_max_reached_short": "Maximum {max} audio file(s) reached. Tap Done.",
        "vid_aud_saved": "✓  Audio @aud{n} saved.  ({count}/{max})",
        "vid_aud_saved_short": "✓  @aud{n} saved  ({count}/{max})",

        "vid_attached_files_label": "\n  <b>Attached files:</b>\n{lines}\n  Note: these labels are just for your own reference —\n  the AI doesn't read them. Describe each file in words\n  in your prompt.\n",
        "vid_attach_n_imgs": "  ◈  {count} image(s) → @img1",
        "vid_attach_n_vids": "  ◈  {count} video(s) → @vid1",
        "vid_attach_n_auds": "  ◈  {count} audio(s) → @aud1",
        "vid_attach_start_attached": "  ◈  Start frame attached\n",
        "vid_attach_end_attached": "  ◈  End frame attached\n",
        "vid_now_select_resolution": "  Now select resolution:",

        "vid_hgtr_quality_desc": (
            "  Select quality mode:\n\n"
            "  <b>Precision</b>  —  highest accuracy, slower\n"
            "  <b>Speed</b>  —  faster processing, lower cost"
        ),
        "vid_btn_precision": "◈  Precision",
        "vid_btn_speed": "◈  Speed",

        "vid_hga4_select_ar": "  Select aspect ratio:",
        "vid_hga4_select_res": "  Select resolution:",
        "vid_hga4_select_style": "  Select talking style:",
        "vid_omni_desc": "  Animate any portrait with voice.\n\n  Select duration:",

        # ── Wallet / top-up flow ────────────────────────────────
        "wallet_title": "◈  <b>Your Wallet</b>",
        "wallet_balance": "  Balance     <b>{coins} coins</b>  (≈ ${usd})",
        "wallet_rate": "  Rate          1 coin  =  $0.05",
        "wallet_min_topup": "  Min top-up   $2.00  =  40 coins",
        "wallet_btn_add_coins": "＋  Add Coins",
        "wallet_btn_referral": "◈  Referral Program",

        "wallet_topup_title": "＋  <b>Add Coins</b>",
        "wallet_topup_rate_line": "  1 coin  =  <b>$0.05</b>",
        "wallet_topup_min_line": "  $2.00   =  <b>40 coins</b>  ← minimum",
        "wallet_topup_5_line": "  $5.00   =  <b>100 coins</b>",
        "wallet_topup_10_line": "  $10.00  =  <b>200 coins</b>",
        "wallet_topup_select_or_custom": "Select amount or enter custom:",
        "wallet_btn_2": "$2  →  40 coins",
        "wallet_btn_5": "$5  →  100 coins",
        "wallet_btn_10": "$10  →  200 coins",
        "wallet_btn_20": "$20  →  400 coins",
        "wallet_btn_custom": "✎  Custom amount",

        "wallet_custom_title": "✎  <b>Custom Amount</b>",
        "wallet_custom_desc": "Type the amount in USD (minimum $2.00):\n\n<i>Example: 7.5</i>",
        "wallet_min_deposit_error": "Minimum deposit is ${min}. Please enter a valid amount (e.g. 2, 5, 10).",
        "wallet_enter_number_error": "Please enter a number (e.g. 5 or 7.50).\n\nType /cancel to exit.",

        "wallet_confirm_title": "◈  <b>Confirm Top-up</b>",
        "wallet_confirm_amount": "  Amount      <b>${amount}</b>",
        "wallet_confirm_receive": "  You receive  <b>{coins} coins</b>",
        "wallet_choose_payment": "Choose payment method:",
        "wallet_btn_pay_stars": "⭐  Pay with Stars ({stars} XTR)",
        "wallet_btn_pay_usdt": "₮  Pay with USDT (TRC20)",

        "wallet_usdt_title": "₮  <b>USDT Payment</b>",
        "wallet_usdt_send_exactly": "  Send exactly  <b>${amount} USDT</b>",
        "wallet_usdt_network": "  Network          <b>TRC20 (Tron)</b>",
        "wallet_usdt_address_label": "  Wallet address:",
        "wallet_usdt_after_sending": "After sending, paste your <b>transaction hash</b> below.\n<i>The system will verify it automatically.</i>",

        "wallet_verifying": "⏳  Verifying transaction...",
        "wallet_verified_title": "✓  <b>Payment Verified</b>",
        "wallet_verified_confirmed": "  Transaction confirmed",
        "wallet_verified_amount": "  Amount received   <b>${amount} USDT</b>",
        "wallet_verified_coins": "  Coins credited     <b>{coins} coins</b>",
        "wallet_verified_balance": "  New balance        <b>{coins} coins</b>",

        "wallet_review_title": "◌  <b>Under Review</b>",
        "wallet_review_body": (
            "  We could not verify your transaction automatically.\n"
            "  Our team will review it manually within 15 minutes.\n\n"
            "  Coins will be credited after confirmation."
        ),

        "wallet_stars_invoice_title": "RetainX Studio — Coins",
        "wallet_stars_invoice_desc": "Top up {coins} coins to your RetainX account",
        "wallet_stars_label": "{coins} Coins",
        "wallet_stars_success_title": "⭐  <b>Payment Successful</b>",
        "wallet_stars_success_body": "  {coins} coins added to your wallet.\n  New balance: <b>{coins2} coins</b>",

        "wallet_topup_confirmed_title": "✓  <b>Top-up Confirmed</b>",
        "wallet_topup_confirmed_body": "  <b>{coins} coins</b> added to your wallet.\n  Balance: <b>{balance} coins</b>",
        "wallet_topup_rejected": "✕  Your top-up was not confirmed. Please contact support.",

        "wallet_btn_yoomoney": "₽  Оплатить картой РФ",
        "wallet_yoomoney_title": "₽  <b>YooMoney Top-up</b>",
        "wallet_yoomoney_rate_line": "  1 coin  =  <b>3.70 ₽</b>",
        "wallet_yoomoney_min_line": "  185 ₽   =  <b>50 coins</b>  ← minimum",
        "wallet_yoomoney_prompt": "Enter the amount in rubles you want to pay:\n\n<i>Example: 500</i>",
        "wallet_yoomoney_min_error": "Minimum deposit is {min} ₽ (50 coins). Please enter a larger amount.",
        "wallet_yoomoney_confirm_title": "₽  <b>YooMoney Payment</b>",
        "wallet_yoomoney_confirm_amount": "  Amount      <b>{amount} ₽</b>",
        "wallet_yoomoney_confirm_coins": "  You receive  <b>{coins} coins</b>",
        "wallet_yoomoney_confirm_note": "Tap the button below to pay. Coins are credited automatically after payment.",
        "wallet_btn_pay_yoomoney": "₽  Оплатить {amount} ₽ картой РФ",
        "wallet_yoomoney_success_title": "✓  <b>Payment Received</b>",
        "wallet_yoomoney_success_body": "  <b>{coins} coins</b> added to your wallet.\n  Payment: <b>{amount} ₽</b>",

        "wallet_btn_card": "💳  Pay by Card RF",
        "wallet_card_title": "💳  <b>Card Payment (RF)</b>",
        "wallet_card_rate_line": "  1 coin  =  <b>3.70 ₽</b>",
        "wallet_card_min_line": "  185 ₽   =  <b>50 coins</b>  ← minimum",
        "wallet_card_prompt": "Enter the amount in rubles you want to pay:\n\n<i>Example: 500</i>",
        "wallet_card_min_error": "Minimum deposit is {min} ₽ (50 coins). Please enter a larger amount.",
        "wallet_card_confirm_title": "💳  <b>Card Payment</b>",
        "wallet_card_confirm_amount": "  Amount        <b>{amount} ₽</b>",
        "wallet_card_confirm_coins": "  You receive   <b>{coins} coins</b>",
        "wallet_card_number_label": "  Card number:",
        "wallet_card_note": "Transfer the amount to the card above.\nThen send a <b>screenshot</b> or <b>check number</b> as confirmation.",
        "wallet_card_submitted_title": "⏳  <b>Under Review</b>",
        "wallet_card_submitted_body": "  Your payment is being reviewed.\n  Coins will be credited within 15 minutes.",
        "wallet_card_success_title": "✓  <b>Payment Confirmed</b>",
        "wallet_card_success_body": "  <b>{coins} coins</b> added to your wallet.\n  New balance: <b>{balance} coins</b>",
        "wallet_card_rejected_title": "✕  <b>Payment Not Confirmed</b>",
        "wallet_card_rejected_body": "  Your card payment could not be confirmed.\n  Please contact @RetainXStudio.",

        "wallet_session_expired": "⚠️  Session expired. Please start a new top-up from the wallet menu.",
        "wallet_tx_already_used": "⚠️  This transaction has already been used. Please use a different transaction.",

        "wallet_referral_bonus_title": "◈  <b>Referral Bonus</b>",
        "wallet_referral_bonus_body": "  Your referral made a payment.\n  You received <b>{bonus} ◈</b> ({percentage}%) as a referral bonus.",

        "referral_friend_joined": "👤  <b>New referral!</b>\n\n  {username} joined via your link.\n  You'll earn a bonus when they make their first purchase.",

        "wallet_referral_title": "◈  <b>Referral Program</b>",
        "wallet_referral_tier_line": "  ◉  <b>{name}</b>  →  {next}",
        "wallet_referral_tier_max": "  ★  <b>{name}</b>  ·  Max Level",
        "wallet_referral_rate": "  Earn  <b>{first}%</b> first payment  ·  <b>{repeat}%</b> repeat",
        "wallet_referral_stat_invited": "Friends invited",
        "wallet_referral_stat_buyers": "Made a purchase",
        "wallet_referral_stat_balance": "Referral balance",
        "wallet_referral_stat_total": "Total earned",
        "wallet_referral_join_bonus_note": "🎁  Each friend gets +{bonus} bonus coins on join!",
        "wallet_referral_share_btn": "📤  Share my link",
        "wallet_referral_share_text": "I use @RetainXStudioBot for AI video & image generation — Sora 2, Grok, Seedance, HeyGen and more. Join via my link and get +10 bonus coins! 🎁\n",

        "wallet_referral_desc": "  Earn <b>20%</b> from your referral's first payment\n  and <b>10%</b> from every subsequent one.\n  Earnings go to your referral balance in ₽.",
        "wallet_referral_balance_line": "  Referral balance   <b>{balance} ₽</b>",
        "wallet_referral_total_line": "  Total earned         <b>{total} ₽</b>",
        "wallet_referral_stats_line": "  Referrals:  <b>{count}</b>  ·  Made purchase:  <b>{buyers}</b>",
        "wallet_referral_my_list_btn": "👥  My Referrals ({count})",
        "wallet_referral_list_title": "👥  <b>My Referrals</b>",
        "wallet_referral_list_empty": "  No referrals yet.\n  Share your link to start earning!",
        "wallet_referral_list_header": "  <b>{count} total</b>  ·  {buyers} made a purchase",
        "wallet_referral_sub_followers": "👥 {n} followers",
        "wallet_referral_sub_buyers": "🛒 {n} purchases",
        "wallet_referral_blogger_totals": "  Bloggers total: {sub} followers  ·  {sub_buyers} purchases",
        "wallet_referral_promo_btn": "🎟  My Promo Code",

        "promo_btn": "🎟  Promo Code",
        "promo_active_btn": "🎟  Promo: {code}  (−{pct}%)",
        "promo_cancel_btn": "✕  Cancel Promo Code",
        "promo_enter_title": "◈  <b>Promo Code</b>",
        "promo_enter_desc": "  Enter a promo code to get 30% off\n  your first coin top-up.",
        "promo_invalid": "  ✕  Promo code not found.",
        "promo_own_code": "  ✕  You cannot use your own promo code.",
        "promo_already_used": "  ✕  You have already used a promo code.",
        "promo_not_first": "  ✕  Promo codes apply to your first top-up only.",
        "promo_applied": "  ✓  Promo <b>{code}</b> applied  ·  <b>−{pct}%</b> off",
        "promo_cancelled": "  Promo code removed.",
        "wallet_confirm_original": "  Without promo     <b>{amount}</b>",
        "wallet_confirm_discounted": "  You pay                <b>{discounted}</b>  <i>(−{pct}%)</i>",
        "my_promo_title": "◈  <b>My Promo Code</b>",
        "my_promo_none": "  You don't have a promo code yet.\n  Create one and share it with your audience.",
        "my_promo_create_btn": "✦  Create Promo Code",
        "my_promo_code_label": "  Code        <b>{code}</b>",
        "my_promo_discount_label": "  Discount   <b>−{pct}%</b>  ·  first top-up only",
        "my_promo_uses_label": "  Used          <b>{uses} times</b>",
        "my_promo_share_hint": "  Share this code in your posts and videos.",

        "wallet_referral_link_label": "Your link:",
        "wallet_referral_share": "  Share it and earn passively.",
        "wallet_referral_withdraw_btn": "₽  Withdraw {amount} ₽",
        "wallet_referral_withdraw_unavailable": "◌  Min withdrawal: {min} ₽",
        "wallet_referral_withdraw_pending": "◌  Withdrawal pending...",
        "wallet_referral_withdraw_low_alert": "Minimum withdrawal is {min} ₽. Keep earning!",
        "wallet_referral_withdraw_title": "₽  <b>Withdraw Referral Balance</b>",
        "wallet_referral_withdraw_amount": "  Amount to withdraw   <b>{amount} ₽</b>",
        "wallet_referral_enter_requisites": "Enter your bank card number or payment requisites\n(card number, phone for SBP, etc.):",
        "wallet_referral_requisites_invalid": "Please enter valid requisites (card number, phone, etc.).",
        "wallet_referral_withdraw_submitted_title": "✓  <b>Withdrawal Request Submitted</b>",
        "wallet_referral_withdraw_submitted_body": "  Amount: <b>{amount} ₽</b>\n\n  Our team will process it manually within 24 hours.",
        "wallet_referral_withdraw_paid_title": "✓  <b>Withdrawal Processed</b>",
        "wallet_referral_withdraw_paid_body": "  <b>{amount} ₽</b> has been sent to your requisites.",
        "wallet_referral_withdraw_rejected_title": "◌  <b>Withdrawal Rejected</b>",
        "wallet_referral_withdraw_rejected_body": "  Your withdrawal of <b>{amount} ₽</b> was rejected.\n  The amount has been returned to your referral balance.\n  Contact @RetainXStudio for details.",

        # ── Order history flow ──────────────────────────────────
        "order_history_title": "◈  <b>Order History</b>",
        "order_history_empty": "  You have no orders yet.\n\n  Start generating to see your history here.",
        "order_history_total": "  Total orders    <b>{total}</b>",
        "order_history_completed": "  Completed       <b>{delivered}</b>",
        "order_history_spent": "  Coins spent     <b>{spent}◈</b>",
        "order_history_tap_to_view": "  Tap any order to view details:",
        "order_not_found": "Order not found",
        "order_detail_title": "◈  <b>Order #{oid}</b>",
        "order_detail_status": "  Status    {emoji}  <b>{status}</b>",
        "order_detail_model": "  Model     <b>{tool}</b>",
        "order_detail_coins": "  Coins      {coins}◈",
        "order_detail_date": "  Date        {date}",
        "order_detail_resolution": "  Resolution    {res}",
        "order_detail_aspect_ratio": "  Aspect ratio  {ar}",
        "order_detail_duration": "  Duration       {dur} sec",
        "order_detail_quality": "  Quality          {quality}",
        "order_detail_audio": "  Audio            Yes",
        "order_detail_language": "  Language      {lang}",
        "order_detail_prompt_label": "  Prompt:",
        "order_btn_repeat": "↺  Repeat this order",
        "order_btn_back": "← Back",
        "order_repeat_title": "◈  <b>Repeat Order</b>",
        "order_repeat_model": "  Model     <b>{tool}</b>",
        "order_repeat_resolution": "  Resolution   {res}",
        "order_repeat_aspect": "  Aspect        {ar}",
        "order_repeat_duration": "  Duration      {dur} sec",
        "order_repeat_cost": "  Cost           <b>{coins} coins</b>",
        "order_repeat_prev_prompt": "  Previous prompt:",
        "order_repeat_enter_prompt": "  Enter your prompt (or send same as above):",
        "order_status_processing": "Processing",
        "order_status_delivered": "Delivered",
        "order_status_cancelled": "Cancelled",
        "order_your_result": "◈  Your generated result",

        # ── Maintenance ──────────────────────────────────────────
        "maintenance_msg": "🔧 <b>Maintenance</b>\n\nThe bot is temporarily unavailable. Please try again later.",
        "maintenance_alert": "🔧 Maintenance. The bot is temporarily unavailable.",

        # ── Unlimited pass UI ────────────────────────────────────
        "unlim_active_line": "\n{emoji} <b>Unlimited {name} active</b> — {mins}m {secs}s left\n",
        "unlim_btn_buy": "⚡  Unlimited — buy a plan",
        "unlim_btn_active": "⚡  Unlimited {name} active ✓",
        "unlim_active_toast": "⚡ Unlimited is active!",
        "unlim_buy_title": "⚡  <b>Unlimited Plans</b>",
        "unlim_buy_balance": "  Your balance:  <b>{coins}◈</b>",
        "unlim_buy_select": "  Choose a plan:",
        "unlim_btn_info": "ℹ  Plan details",
        "unlim_dur_1h": "1 hour  —  {coins}◈",
        "unlim_dur_2h": "2 hours  —  {coins}◈  (−10%/h)",
        "unlim_dur_3h": "3 hours  —  {coins}◈  (−20%/h)",
        "unlim_select_duration": "  Choose duration:",
        "unlim_not_enough": "Not enough coins. Need {need}◈, you have {have}◈.",
        "unlim_confirm_title": "⚡  <b>Confirm Purchase</b>",
        "unlim_confirm_tier": "  Plan:              <b>{name}</b>",
        "unlim_confirm_dur": "  Duration:         <b>{hours} h</b>",
        "unlim_confirm_cost": "  Cost:               <b>{cost}◈</b>",
        "unlim_confirm_balance": "  Your balance:   <b>{coins}◈</b>",
        "unlim_btn_activate": "✓  Activate — {cost}◈",
        "unlim_error_retry": "Error. Please try again.",
        "unlim_no_balance": "Not enough coins. Top up your balance.",
        "unlim_activated_title": "⚡  <b>Unlimited {name} activated!</b>",
        "unlim_activated_body": "  Active until  <b>{time}</b>  ({hours} h)\n  Generate as much as you want!\n\n  Deducted:  <b>{cost}◈</b>",
        "unlim_info_title": "⚡  <b>Unlimited Plans</b>",
        "unlim_info_body": "  Generate unlimited for 1, 2, or 3 hours —\n  no coins deducted per request.\n\n  Choose a plan to learn more:",
        "unlim_btn_buy_plan": "🛒  Buy {label}",
        "unlim_tier_std_info": (
            "  ✓  Seedance 2.0 Fast · Wan 2.7 · Grok 1.5\n"
            "  ✓  LTX 2.3 Pro · Veo 3.1 Lite · Kling 3.0 · Kling O3\n"
            "  ✕  Premium video (Veo 3.1, Sora 2)\n"
            "  ✕  Audio / voiceover\n"
            "  ✕  Avatars\n"
            "  ⬆  Resolution up to 720p"
        ),
        "unlim_tier_pro_info": (
            "  ✓  Everything from Standard (up to 1080p)\n"
            "  ✓  Premium: Veo 3.1 · Veo 3.1 Fast · Sora 2\n"
            "  ✓  Audio / voiceover\n"
            "  ✕  Avatars\n"
            "  ⬆  Resolution up to 1080p"
        ),
        "unlim_tier_vip_info": (
            "  ✓  Everything from Pro\n"
            "  ✓  Resolution up to 4K\n"
            "  ✕  Avatars"
        ),
        "unlim_page_std": (
            "⚡  <b>Unlimited Standard</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Generate videos and images without limits\n"
            "  — no coins deducted per request.\n\n"
            "<b>📹 Video — Standard:</b>\n"
            "  • Seedance 2.0 Fast\n"
            "  • Wan 2.7\n"
            "  • LTX 2.3 Pro\n"
            "  • Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5  <i>(max. 480p)</i>\n\n"
            "<b>🎬 Video — Kling:</b>\n"
            "  • Kling 3.0\n"
            "  • Kling O3\n\n"
            "  ✕  Premium video (Veo 3.1, Sora 2)\n"
            "  ✕  Audio & Voice\n"
            "  ✕  Avatars\n\n"
            "  ⬆  Resolution: up to 720p\n\n"
            "<b>💰 Pricing:</b>\n"
            "  1 hour   →  <b>{p1}◈</b>\n"
            "  2 hours  →  <b>{p2}◈</b>  <i>(−10% per hour)</i>\n"
            "  3 hours  →  <b>{p3}◈</b>  <i>(−20% per hour)</i>"
        ),
        "unlim_page_pro": (
            "⚡⚡  <b>Unlimited Pro</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Everything from Standard plus Premium models\n"
            "  and audio — up to 1080p.\n\n"
            "<b>📹 Video — Standard (up to 1080p):</b>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • LTX 2.3 Pro · Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5\n\n"
            "<b>🎬 Video — Kling (up to 1080p):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 Premium video (up to 1080p):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 Audio & Voice:</b>\n"
            "  • ElevenLabs · Artlist & others\n\n"
            "  ✕  Avatars\n\n"
            "  ⬆  Resolution: up to 1080p\n\n"
            "<b>💰 Pricing:</b>\n"
            "  1 hour   →  <b>{p1}◈</b>\n"
            "  2 hours  →  <b>{p2}◈</b>  <i>(−10% per hour)</i>\n"
            "  3 hours  →  <b>{p3}◈</b>  <i>(−20% per hour)</i>"
        ),
        "unlim_page_vip": (
            "♛  <b>Unlimited VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Maximum plan — everything from Pro\n"
            "  with resolution up to 4K.\n\n"
            "  ✓  All models from Pro\n\n"
            "<b>📹 Standard video (up to 4K):</b>\n"
            "  • LTX 2.3 Pro  <i>(720p / 1080p / 2K / 4K)</i>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • Veo 3.1 Lite · Grok Imagine 1.5\n\n"
            "<b>🎬 Kling (up to 4K):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 Premium video (up to 4K):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 Audio & Voice</b>\n\n"
            "  ✕  Avatars\n\n"
            "  ⬆  Resolution: up to 4K\n\n"
            "<b>💰 Pricing:</b>\n"
            "  1 hour   →  <b>{p1}◈</b>\n"
            "  2 hours  →  <b>{p2}◈</b>  <i>(−10% per hour)</i>\n"
            "  3 hours  →  <b>{p3}◈</b>  <i>(−20% per hour)</i>"
        ),
        "unlim_tier_title": "⚡  <b>Unlimited {name}</b>",
        "unlim_info_tier_btn": "{emoji}  {name}  —  from {coins}◈",
    },
    "ru": {
        "welcome_title": "◈  <b>Добро пожаловать в RetainX Studio</b>",
        "welcome_body": (
            "  Самый быстрый и доступный способ\n"
            "  генерации AI видео, изображений и аудио.\n\n"
            "  ◉  Kling 3.0  ·  Veo 3.1  ·  Sora 2\n"
            "  ◉  Midjourney  ·  Flux  ·  Seedance\n"
            "  ◉  HeyGen  ·  ElevenLabs  ·  LTX\n\n"
            "  До <b>3× дешевле</b> любого конкурента.\n"
            "  Результат за <b>~2 минуты.</b>"
        ),
        "welcome_bonus": "  🎁  <b>{bonus} монет</b> начислено на ваш счёт.\n  Баланс   <b>{coins} монет</b>",
        "what_create": "Что бы вы хотели создать?",
        "choose_option": "Выберите вариант:",

        "main_menu_title": "◈  <b>RetainX Studio</b>",
        "main_menu_balance": "  Баланс   <b>{coins} монет</b>",
        "main_menu_desc": "  Генерация AI видео, изображений и аудио\n  по самым выгодным ценам.",
        "maintenance_banner": "⚠️  <b>Технические работы: 10 – 13 июля</b>\n      Бот может быть временно недоступен.\n",

        "btn_video_generation": "▸  Генерация видео",
        "btn_image_generation": "▸  Генерация изображений",
        "btn_audio_voice": "▸  Аудио и голос",
        "btn_wallet_coins": "◈  Кошелёк  ·  {coins} монет",
        "btn_pricing": "◎  Цены",
        "btn_support": "◌  Поддержка",
        "btn_language": "◐  Язык",
        "btn_start_generating": "▸  Начать генерацию",
        "btn_view_pricing": "◎  Смотреть цены",
        "btn_back": "←  Назад",
        "btn_help": "📖  Справка",

        # ── Help pages ──
        "help_main_text": (
            "📖  <b>Справка — RetainX Studio</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Выберите раздел для подробной информации:"
        ),
        "help_start_text": (
            "🚀  <b>Как начать работу</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Система монет</b>\n"
            "  1 монета = $0.05   ·   $1 = 20 монет\n"
            "  Минимальное пополнение: $2 (40 монет)\n\n"
            "  <b>Первые шаги</b>\n"
            "  1 · Выбери тип — Видео, Фото или Аудио\n"
            "  2 · Выбери модель и нужные параметры\n"
            "  3 · Напиши промпт на любом языке\n"
            "  4 · Жди результат ~2 минуты\n\n"
            "  <b>Стартовый бонус</b>\n"
            "  20 монет бесплатно при первом запуске 🎁\n\n"
            "  <b>Промо-коды</b>\n"
            "  Введи /promo [КОД] для активации\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_video_text": (
            "🎬  <b>Генерация видео</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Стандартные</b>  (доступны всем)\n"
            "  Seedance 2.0 Fast · Wan 2.7 · LTX 2.3 Pro\n"
            "  Veo 3.1 Lite · Grok 1.5\n\n"
            "  <b>Kling</b>  (доступны всем)\n"
            "  Kling 3.0 · Kling O3  ·  до 4K\n\n"
            "  <b>Премиум</b>  (Безлимит Pro / VIP)\n"
            "  Veo 3.1 Full · Veo 3.1 Fast · Sora 2 Pro\n\n"
            "  <b>Аватар и дубляж</b>\n"
            "  HeyGen · ElevenLabs · Lipsync · OmniHuman\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "  Нажмите на раздел для подробностей ↓"
        ),
        "help_vid_std_text": (
            "▸  <b>Стандартные видео-модели</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Seedance 2.0 Fast</b>\n"
            "  480p / 720p  ·  4–15 сек\n"
            "  от 5◈ (480p 4с)  до 45◈ (720p 15с)\n\n"
            "<b>Wan 2.7</b>\n"
            "  720p / 1080p  ·  2–15 сек\n"
            "  от 4◈ (720p 2с)  до 45◈ (1080p 15с)\n\n"
            "<b>LTX 2.3 Pro</b>\n"
            "  720p / 1080p / 2K / 4K  ·  6–10 сек\n"
            "  от 6◈ (720p)  до 75◈ (4K 10с)\n\n"
            "<b>Veo 3.1 Lite</b>\n"
            "  720p / 1080p  ·  4–8 сек\n"
            "  от 3◈ (720p 4с)  до 8◈ (1080p 8с)\n\n"
            "<b>Grok 1.5</b>\n"
            "  До 15 сек  ·  4◈/сек  (60◈ за 15с)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_prem_text": (
            "★  <b>Премиум видео-модели</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "  ⚠️ Требуется Безлимит Pro / VIP\n\n"
            "<b>Veo 3.1 Full</b>  (лучшее качество Google)\n"
            "  720p / 1080p / 4K  ·  4–8 сек\n"
            "  от 15◈ (720p 4с)  до 58◈ (4K 8с)\n\n"
            "<b>Veo 3.1 Fast</b>\n"
            "  720p / 1080p / 4K  ·  4–8 сек\n"
            "  от 8◈ (720p 4с)  до 40◈ (4K 8с)\n\n"
            "<b>Sora 2 Pro</b>  (OpenAI)\n"
            "  720p / 1080p  ·  4–12 сек\n"
            "  от 26◈ (720p 4с)  до 114◈ (1080p 12с)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_kling_text": (
            "◉  <b>Kling — видео-модели</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Kling 3.0</b>\n"
            "  720p / 1080p / 4K  ·  3–15 сек\n"
            "  от 4◈ (720p 3с)  до 75◈ (4K 15с)\n\n"
            "<b>Kling O3</b>  (ультра-качество)\n"
            "  720p / 1080p / 4K  ·  3–15 сек\n"
            "  от 4◈ (720p 3с)  до 75◈ (4K 15с)\n\n"
            "  ✓ Точное следование промпту\n"
            "  ✓ Фотореалистичные сцены\n"
            "  ✓ Поддержка изображения-референса\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_avatar_text": (
            "◌  <b>Аватар и дубляж</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>HeyGen Avatar</b>\n"
            "  720p / 1080p  ·  1–15 мин  ·  60◈/мин\n\n"
            "<b>ElevenLabs Dubbing</b>\n"
            "  Профессиональный дубляж  ·  60◈/мин\n"
            "  29 языков\n\n"
            "<b>Lipsync</b>\n"
            "  Синхронизация губ с аудио  ·  60◈/мин\n\n"
            "<b>OmniHuman / Aurora Avatar</b>\n"
            "  Аватар по фото + голосу\n"
            "  60◈/мин (OmniHuman)  ·  54◈/мин (Aurora)\n\n"
            "  Форматы: MP4, MOV, AVI\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_images_text": (
            "🖼  <b>Генерация изображений</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Nano Banana Pro</b>   1K–2K: 3◈  ·  4K: 4◈\n"
            "  <b>Nano Banana 2</b>     1K–2K: 2◈  ·  4K: 3◈\n"
            "  <b>Seedream 5.0 Pro</b>  1K: 1◈  ·  2K: 2◈\n"
            "  <b>GPT Image 2</b>       1K: 1◈  ·  2K: 2◈  ·  4K: 3◈\n"
            "  <b>Wan 2.7 Pro</b>       4K: 2◈\n"
            "  <b>Flux 2.0 Pro</b>      1K–2K: 1◈\n"
            "  <b>Ideogram v3</b>       Turbo/Balanced: 1◈  ·  Quality: 2◈\n"
            "  <b>Topaz Upscaler</b>    2K: 2◈  ·  4K: 3◈  ·  8K: 6◈\n\n"
            "  Форматы: 1:1 · 16:9 · 9:16 · 3:4 и другие\n"
            "  Референс-изображения: до 14 штук\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_audio_text": (
            "🔊  <b>Аудио и озвучка</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>ElevenLabs Voiceover</b>\n"
            "  Профессиональная AI-озвучка текста\n\n"
            "  ✓ 1000+ голосов\n"
            "  ✓ Управление эмоциями и стилем речи\n"
            "  ✓ Настройка стабильности голоса\n"
            "  ✓ Эффекты обработки\n"
            "  ✓ Скорость речи\n"
            "  ✓ 30+ языков\n\n"
            "  Доступно с пакетом Безлимит Pro / VIP\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_text": (
            "◈  <b>Кошелёк и оплата</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Баланс хранится в монетах RetainX.\n"
            "  Монеты списываются автоматически\n"
            "  при каждой генерации.\n\n"
            "  Выберите раздел для подробностей:"
        ),
        "help_wallet_rates_text": (
            "◎  <b>Курсы и лимиты</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Курс монет</b>\n"
            "  1 монета = $0.05\n"
            "  $1 = 20 монет\n"
            "  1 монета ≈ 3.70 ₽\n\n"
            "  <b>Лимиты пополнения</b>\n"
            "  Минимум:       $2.00 = 40 монет\n"
            "  Через Stars:   мин. 40 монет\n"
            "  Через USDT:    мин. $2\n\n"
            "  <b>Способы оплаты</b>\n"
            "  ⭐ Telegram Stars\n"
            "  ₮ USDT (TRC-20)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_stars_text": (
            "⭐  <b>Пополнение через Telegram Stars</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Как пополнить:</b>\n"
            "  1 · Нажмите «◈ Кошелёк» в главном меню\n"
            "  2 · Нажмите «＋ Пополнить монеты»\n"
            "  3 · Выберите «⭐ Stars»\n"
            "  4 · Укажите сумму в монетах (мин. 40)\n"
            "  5 · Оплатите через Telegram — без выхода из приложения\n\n"
            "  Курс Stars → монеты рассчитывается автоматически.\n\n"
            "  ✓ Мгновенное зачисление\n"
            "  ✓ Не нужна карта или криптокошелёк\n"
            "  ✓ Безопасно — встроено в Telegram\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_usdt_text": (
            "₮  <b>Пополнение через USDT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Сеть: TRC-20 (Tron)\n\n"
            "  <b>Как пополнить:</b>\n"
            "  1 · Нажмите «◈ Кошелёк» → «＋ Пополнить»\n"
            "  2 · Выберите «₮ USDT»\n"
            "  3 · Введите сумму в USD (мин. $2)\n"
            "  4 · Переведите USDT на указанный адрес\n"
            "  5 · Сообщите об оплате оператору\n\n"
            "  ✓ Принимаем USDT TRC-20\n"
            "  ✓ Зачисление в течение 15 минут\n"
            "  ✓ Нет комиссии со стороны бота\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_text": (
            "⚡  <b>Безлимитные пакеты</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Безлимитный пакет снимает все ограничения\n"
            "  и открывает доступ к дополнительным моделям.\n\n"
            "  Пакет активен 1, 2 или 3 часа — в течение\n"
            "  этого времени генерируйте без ограничений.\n\n"
            "  <b>Тарифы:</b>\n"
            "  ⚡  Standard  —  от 268◈/ч\n"
            "  ⚡⚡  Pro       —  от 662◈/ч\n"
            "  ♛   VIP       —  от 1619◈/ч\n\n"
            "  Нажмите на тариф для подробностей ↓\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_std_text": (
            "⚡  <b>Безлимит Standard</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Цены:</b>\n"
            "  1 ч  —  268◈\n"
            "  2 ч  —  482◈  (экономия 10%)\n"
            "  3 ч  —  642◈  (экономия 20%)\n\n"
            "  <b>Доступные модели:</b>\n"
            "  ✓ Seedance 2.0 Fast  ·  Wan 2.7\n"
            "  ✓ LTX 2.3 Pro  ·  Veo 3.1 Lite\n"
            "  ✓ Grok 1.5\n"
            "  ✓ Kling 3.0  ·  Kling O3\n\n"
            "  <b>Макс. разрешение:</b>  720p\n\n"
            "  ✕ Премиум-модели (Veo Full, Sora)\n"
            "  ✕ Аватар и дубляж\n"
            "  ✕ Генерация аудио\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_pro_text": (
            "⚡⚡  <b>Безлимит Pro</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Цены:</b>\n"
            "  1 ч  —  662◈\n"
            "  2 ч  —  1192◈  (экономия 10%)\n"
            "  3 ч  —  1589◈  (экономия 20%)\n\n"
            "  <b>Доступные модели:</b>\n"
            "  ✓ Все модели Standard\n"
            "  ✓ Veo 3.1 Full  ·  Veo 3.1 Fast\n"
            "  ✓ Sora 2 Pro\n"
            "  ✓ Kling 3.0  ·  Kling O3\n"
            "  ✓ ElevenLabs Voiceover (аудио)\n\n"
            "  <b>Макс. разрешение:</b>  1080p\n\n"
            "  ✕ Аватар и дубляж\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_vip_text": (
            "♛  <b>Безлимит VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Цены:</b>\n"
            "  1 ч  —  1619◈\n"
            "  2 ч  —  2914◈  (экономия 10%)\n"
            "  3 ч  —  3886◈  (экономия 20%)\n\n"
            "  <b>Доступные модели:</b>\n"
            "  ✓ Все модели Standard и Pro\n"
            "  ✓ Veo 3.1 Full  ·  Sora 2 Pro\n"
            "  ✓ Kling 3.0  ·  Kling O3\n"
            "  ✓ ElevenLabs Voiceover (аудио)\n\n"
            "  <b>Макс. разрешение:</b>  4K\n\n"
            "  ✓ Полный доступ ко всем функциям\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_ref_text": (
            "👥  <b>Реферальная программа</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Поделитесь ссылкой → друг регистрируется\n"
            "  и пополняет → вы получаете % от каждого\n"
            "  пополнения реферала.\n\n"
            "  <b>Уровни вознаграждений:</b>\n"
            "  Стартер (0–5 рефералов)\n"
            "    Первое пополн.  20%  ·  Повторные  10%\n\n"
            "  Партнёр (6–15 рефералов)\n"
            "    Первое пополн.  22%  ·  Повторные  12%\n\n"
            "  Про (16+ рефералов)\n"
            "    Первое пополн.  25%  ·  Повторные  15%\n\n"
            "  <b>Блогерские промо-коды</b>\n"
            "  Работают как реферальная ссылка.\n"
            "  Новый пользователь вводит /promo КОД.\n\n"
            "  Ваша ссылка: ◈ Кошелёк → Реферальная программа\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_support_text": (
            "💬  <b>Поддержка</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Возник вопрос или проблема?\n"
            "  Напишите нам напрямую:\n\n"
            "  @RetainXStudio\n\n"
            "  <b>Время ответа:</b>  обычно до 1 часа\n\n"
            "  <b>С чем помогаем:</b>\n"
            "  ✓ Видео / фото не пришло\n"
            "  ✓ Некорректное списание монет\n"
            "  ✓ Проблемы с пополнением\n"
            "  ✓ Технические ошибки\n"
            "  ✓ Вопросы по моделям\n\n"
            "  По промо-кодам и партнёрству —\n"
            "  также пишите в @RetainXStudio\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        # ── Help button labels ──
        "help_btn_start":       "🚀  Как начать",
        "help_btn_video":       "🎬  Генерация видео",
        "help_btn_vid_std":     "▸  Стандартные модели",
        "help_btn_vid_prem":    "★  Премиум модели",
        "help_btn_vid_kling":   "◉  Kling",
        "help_btn_vid_avatar":  "◌  Аватар и дубляж",
        "help_btn_images":      "🖼  Генерация изображений",
        "help_btn_audio":       "🔊  Аудио и озвучка",
        "help_btn_wallet":      "◈  Кошелёк и оплата",
        "help_btn_wallet_rates":"◎  Курсы и лимиты",
        "help_btn_wallet_stars":"⭐  Telegram Stars",
        "help_btn_wallet_usdt": "₮  USDT / Крипто",
        "help_btn_unlim":       "⚡  Безлимитные пакеты",
        "help_btn_unlim_std":   "⚡  Standard",
        "help_btn_unlim_pro":   "⚡⚡  Pro",
        "help_btn_unlim_vip":   "♛  VIP",
        "help_btn_ref":         "👥  Реферальная программа",
        "help_btn_support":     "💬  Поддержка",

        "audio_title": "◌  <b>Аудио и голос</b>",
        "audio_body": "  Скоро будет доступно.\n\n  Мы интегрируем инструменты синтеза\n  речи и генерации музыки.\n\n  Следите за обновлениями.",
        "audio_pro_vip_body": "  Аудио и голос доступны на тарифах\n  безлимит <b>Про</b> и <b>VIP</b>.\n\n  Перейдите на более высокий тариф,\n  чтобы получить доступ к синтезу речи\n  и генерации аудио.",
        "audio_unlimited_only": "  Генерация войсовера доступна в рамках\n  <b>безлимитной подписки</b>.\n\n  Оформите безлимитный план для доступа\n  к AI-войсоверу с полным каталогом голосов.",

        "tts_coin_menu_body":   "  Генерируйте AI-войсовер за монеты.\n  Выберите модель TTS:",
        "tts_select_voice":     "Выберите голос:",
        "tts_page_indicator":   "Стр. {page}/{total}",
        "tts_voice_card_prompt":"  Прослушайте превью, затем выберите этот голос.",
        "tts_btn_preview":      "🎵  Превью",
        "tts_btn_choose":       "✓  Выбрать этот голос",
        "tts_enter_text_prompt":"  Введите текст для озвучки.\n  Максимум {max} символов.",
        "tts_text_too_long":    "  Текст слишком длинный (макс. {max} символов).\n  Сократите его и попробуйте снова.",
        "tts_order_summary_title": "◈  <b>Сводка заказа</b>",
        "tts_voice_label":      "  Голос:    <b>{name}</b>",
        "tts_model_label":      "  Модель:   {model}",
        "tts_cost_label":       "  Стоимость: ",
        "tts_balance_label":    "  Баланс:   ",
        "tts_text_label":       "  Текст:",
        "tts_confirm_btn":      "Генерировать ({coins}◈)",
        "tts_edit_text_btn":    "Изменить текст",
        "tts_order_placed_title": "◈  <b>Заказ #{oid} принят</b>",
        "tts_voice_row":        "  Голос     <b>{name}</b>",
        "tts_coins_deducted":   "  {coins}◈ списано с вашего баланса",
        "tts_estimated_delivery":"  Примерно: ~{minutes} мин",
        "tts_will_deliver":     "  Аудио будет отправлено сюда, когда будет готово.",
        "tts_session_expired":  "Сессия истекла, начните заново.",
        "tts_insufficient_coins":"Недостаточно монет. Пополните баланс.",

        "vid_subcat_tier_alert": "Эта категория не входит в ваш текущий тариф.",

        "vo_low_balance_notice": "Низкий баланс: {coins} монет — пополните перед заказом.",
        "vo_select_model": "  Выберите модель ИИ-голоса:",
        "vo_select_category": "  Выберите категорию голоса:",
        "vo_select_gender": "  Выберите пол голоса:",
        "vo_select_age": "  Выберите возраст голоса:",
        "vo_select_voice": "  Выберите голос:",
        "vo_btn_listen_all": "🔊  Прослушать всех ({count})",
        "vo_listen_all_sending": "🔊 Отправляю превью…",
        "vo_select_language": "  Выберите язык:",
        "vo_preview_error": "⚠️  Не удалось загрузить превью. Попробуйте ещё раз.",
        "vo_voice_gender_label": "  Пол            {gender}",
        "vo_voice_age_label": "  Возраст      {age}",
        "vo_voice_category_label": "  Категория   {category}",
        "vo_voice_model_label": "  Модель       {model}",
        "vo_voice_language_label": "  Язык          {language}",
        "vo_btn_choose_voice": "✓  Выбрать этот голос",
        "vo_btn_listen": "🎧  Прослушать пример",
        "vo_btn_change_language": "🌐  Изменить язык  ·  {language}",
        "vo_preview_caption": "🎧  {voice}  —  {language}  ({model})",
        "vo_voice_stability_label": "  Стабильность   {pct}%",
        "vo_voice_effect_label": "  Эффект            {effect}",
        "vo_btn_stability": "🎚  Стабильность  ·  {pct}%",
        "vo_select_stability": "  Настройте стабильность голоса.\n  Меньше — выразительнее, больше — стабильнее.",
        "vo_btn_effect": "🎭  Эффект  ·  {effect}",
        "vo_select_effect": "  Выберите эффект голоса:",
        "vo_effect_preview_caption": "🎭  {effect}  —  пример эффекта",
        "vo_btn_done": "✓  Готово",
        "vo_stability_label": "  Стабильность   <b>{pct}%</b>",
        "vo_effect_label": "  Эффект            <b>{effect}</b>",
        "vo_voice_emotion_label": "  Эмоция        {emotion}",
        "vo_btn_emotion": "🙂  Эмоция  ·  {emotion}",
        "vo_select_emotion": "  Выберите эмоцию:",
        "vo_emotion_label": "  Эмоция           <b>{emotion}</b>",
        "vo_voice_speed_label": "  Скорость     {speed}x",
        "vo_btn_speed": "⏱  Скорость  ·  {speed}x",
        "vo_select_speed": "  Настройте скорость речи.",
        "vo_speed_label": "  Скорость        <b>{speed}x</b>",
        "vo_enter_text": "  Введите текст, который должен озвучить этот голос:",
        "vo_edit_text_prompt": "  Введите новый текст для этого голоса:",
        "vo_order_summary_title": "◈  <b>Сводка заказа озвучки</b>",
        "vo_voice_label": "  Голос          <b>{name}</b>",
        "vo_model_label": "  Модель        <b>{model}</b>",
        "vo_language_label": "  Язык           <b>{language}</b>",
        "vo_text_label": "  Текст",
        "vo_cost_label": "  Стоимость   ",
        "vo_balance_label": "  Баланс       ",
        "vo_btn_confirm": "✓  Подтвердить  ·  {coins} монет",
        "vo_btn_edit_text": "✎  Изменить текст",
        "vo_session_expired": "Сессия истекла, начните заново.",
        "vo_insufficient_coins": "Недостаточно монет. Пополните кошелёк.",
        "vo_order_placed_title": "✓  <b>Заказ озвучки #{oid} оформлен!</b>",
        "vo_voice_row": "  Голос          <b>{name}</b>",
        "vo_coins_deducted": "  Списано монет   <b>{coins} монет</b>",
        "vo_estimated_delivery": "  Ожидаемое время доставки: ~{minutes} мин",
        "vo_will_deliver": "  Мы доставим аудиофайл прямо в этот чат.",

        "support_title": "◌  <b>Поддержка</b>",
        "support_body": "  Свяжитесь с нами: @RetainXStudio",

        "video_title": "◈  <b>Генерация видео</b>",
        "select_category": "Выберите категорию:",

        "images_title": "◈  <b>Генерация изображений</b>",
        "select_model": "Выберите модель:",

        "pricing_title": "◎  <b>Цены</b>",
        "pricing_body": "  1 монета  =  <b>$0.05</b>\n\n  Выберите категорию для просмотра цен:",
        "btn_image_pricing": "▸  Цены на изображения",
        "btn_video_pricing": "▸  Цены на видео",

        "price_images_title": "◎  <b>Цены на изображения</b>",
        "price_video_title": "◎  <b>Цены на видео</b>",
        "price_video_body": (
            "  Цены зависят от модели, разрешения и длительности.\n"
            "  Выберите модель в разделе «Генерация видео»,\n"
            "  чтобы увидеть точную стоимость в монетах.\n\n"
            "  <b>Примерные тарифы:</b>\n"
            "  Kling 3.0   720p  5s  —  6◈\n"
            "  Veo 3.1     4K    8s  —  58◈\n"
            "  Seedance   1080p 10s  —  60◈\n"
        ),

        "menu_main_menu": "⌂  Главное меню",
        "menu_wallet": "◈  Кошелёк",
        "menu_video": "▸  Видео",
        "menu_images": "▸  Изображения",
        "menu_audio": "▸  Аудио",
        "menu_orders": "≡  Заказы",
        "menu_support": "◌  Поддержка",

        "lang_title": "◐  <b>Язык</b>",
        "lang_desc": "  Выберите предпочитаемый язык:",
        "lang_changed": "✓  Язык обновлён.",

        "coins_word": "монет",

        # ── Image generation flow ──────────────────────────────
        "img_menu_title": "◈  <b>Генерация изображений</b>",
        "img_menu_select": "Выберите модель, чтобы продолжить:",
        "img_price_label": "Цена",
        "img_per_gen": "за генерацию",
        "img_select_ar": "Выберите соотношение сторон:",
        "img_select_quality": "Выберите качество:",
        "img_aspect_ratio_label": "Соотношение сторон",
        "img_quality_label": "Качество",
        "img_cost_label": "Стоимость",
        "img_balance_label": "Ваш баланс",
        "img_attach_optional": "  Прикрепите референс-изображения (необязательно)\n  или пропустите и напишите промпт.",
        "img_btn_add_ref": "◈  Добавить референс  (до {max})",
        "img_btn_skip_prompt": "▸  Пропустить — написать промпт",
        "img_enter_prompt": "Введите промпт:",
        "img_order_summary_title": "◈  <b>Сводка заказа</b>",
        "img_model_label": "Модель",
        "img_prompt_label": "Промпт:",
        "img_btn_confirm": "◈  Подтвердить  ({coins} монет)",
        "img_btn_confirm_free": "◈  Подтвердить  (бесплатно)",
        "img_btn_edit_prompt": "✎  Изменить промпт",
        "img_edit_prompt_prompt": "✎  Введите новый промпт:",
        "img_session_expired": "Сессия истекла. Начните оформление заказа заново.",
        "img_insufficient_coins": "Недостаточно монет. Пополните кошелёк.",
        "img_order_error": "⚠️  Не удалось оформить заказ. Монеты возвращены.",
        "img_order_placed_title": "◌  <b>Заказ #{oid} оформлен</b>",
        "img_model_row": "  Модель     <b>{name}</b>",
        "img_coins_deducted": "  Монеты      <b>{coins} списано</b>",
        "img_estimated_time": "  Ожидаемое время  ~{minutes} мин",
        "img_will_deliver": "  Мы пришлём изображение сюда в ближайшее время.",
        "img_ref_title": "◈  <b>Референс-изображение</b>  ({count}/{max})",
        "img_ref_instructions": (
            "  Отправьте до <b>{max} изображений</b> в качестве референса.\n\n"
            "  <code>@img1</code>, <code>@img2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждое изображение\n"
            "  словами в промпте.\n\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "btn_done": "✓  Готово",
        "img_ref_saved": "✓  Изображение @img{n} сохранено.  ({count}/{max})",
        "img_ref_send_more": "Отправьте ещё или нажмите Готово.",
        "img_ref_max_reached": "Достигнут максимум. Нажмите Готово.",
        "img_ref_max_alert": "Достигнут максимум {max} изображений. Нажмите Готово, чтобы продолжить.",
        "img_ref_required_alert": "Пожалуйста, прикрепите изображение перед продолжением.",
        "img_refs_attached": "  ◈  {count} референс(ов) прикреплено\n",

        # ── Video generation flow ──────────────────────────────
        "vid_menu_title": "◈  <b>Генерация видео</b>",
        "vid_select_category": "Выберите категорию:",
        "vid_low_balance_notice": "Низкий баланс: {coins} монет — пополните перед заказом.",
        "vid_sub_standard": "▸  Стандартное видео",
        "vid_sub_grok": "▸  Grok Видео",
        "vid_sub_premium": "▸  Премиум видео",
        "vid_sub_kling": "▸  Kling видео",
        "vid_sub_avatar": "▸  Аватары и дубляж",
        "vid_select_model": "Выберите модель:",
        "vid_unknown_tool": "Инструмент не найден",
        "vid_resolution_word": "Разрешение",
        "vid_duration_word": "Длительность",
        "vid_sec_word": "сек",
        "vid_type_word": "Тип",
        "vid_avatar_video_word": "Видео-аватар",
        "vid_select_resolution": "  Выберите разрешение:",
        "vid_select_aspect_ratio": "  Выберите соотношение сторон:",
        "vid_select_duration": "  Выберите длительность:",
        "vid_resolution_label": "  Разрешение    {res}",
        "vid_aspect_ratio_label": "  Соотношение сторон  {ar}",
        "vid_duration_label": "  Длительность   {dur} сек",
        "vid_cost_label": "  Стоимость       <b>{coins} монет</b>",
        "vid_cost_label_short": "  Стоимость   <b>{coins} монет</b>",
        "vid_balance_label": "  Баланс        {coins} монет",
        "vid_audio_label": "  Аудио            {audio}",
        "vid_audio_yes": "Да",
        "vid_audio_no": "Нет",
        "vid_include_audio": "  Добавить аудио в видео?",
        "vid_btn_with_audio": "🔊  С аудио",
        "vid_btn_no_audio": "🔇  Без аудио",
        "vid_enter_prompt": "Введите промпт:",
        "vid_btn_confirm": "◈  Подтвердить  ({coins} монет)",
        "vid_btn_edit_prompt": "✎  Изменить промпт",
        "vid_edit_prompt_prompt": "✎  Введите новый промпт:",
        "vid_order_summary_title": "◈  <b>Сводка заказа</b>",
        "vid_model_label": "  Модель          <b>{name}</b>",
        "vid_language_label": "  Язык             {lang}",
        "vid_attachments_label": "\n  Вложения:\n",
        "vid_prompt_label": "  Промпт:",
        "vid_session_expired": "Сессия истекла. Начните оформление заказа заново.",
        "vid_insufficient_coins": "Недостаточно монет. Пополните кошелёк.",
        "vid_avatar_blocked_unlimited": "Аватар-инструменты недоступны в режиме Безлимит.",
        "vid_order_error": "⚠️  Не удалось оформить заказ. Монеты возвращены.",
        "vid_order_placed_title": "◌  <b>Заказ #{oid} оформлен</b>",
        "vid_model_row": "  Модель     <b>{name}</b>",
        "vid_coins_deducted": "  Монеты      <b>{coins} списано</b>",
        "vid_estimated_delivery": "  Ожидаемое время  ~{minutes} мин",
        "vid_will_deliver": "  Результат будет отправлен сюда.",
        "order_ready_caption": (
            "◈  <b>Ваш заказ готов</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Заказ     #{oid}\n"
            "  Модель    {tool}\n\n"
            "  Спасибо, что выбрали RetainX Studio."
        ),

        "vid_grok_title": "◈  <b>Grok Imagine 1.5</b>",
        "vid_grok_resolution_line": "  Разрешение: 720p\n\n  Выберите длительность:",
        "vid_grok_res_select": "  Разрешение: {res}\n\n  Выберите длительность:",
        "vid_grokt_title": "◈  <b>Grok Text-to-Video</b>",
        "vid_groki_title": "◈  <b>Grok Image-to-Video</b>",
        "vid_btn_char_photo":   "Фото персонажа",
        "vid_char_photo_title": "◈  <b>Фото персонажа</b>",
        "vid_char_photo_desc":  "  Отправьте фото персонажа, которого хотите анимировать.\n\n  Модель создаст движение по мотивам этого фото.",
        "vid_grok_mode_select": "  Выберите режим генерации:",
        "vid_grok_mode_fun": "Весёлый",
        "vid_grok_mode_normal": "Обычный",
        "vid_grok_mode_spicy": "Пикантный",
        "vid_grok_extend_prompt": "◈  <b>Grok Extend  +{secs}с</b>\n━━━━━━━━━━━━━━━━━━━━\n\n  Введите промпт для продления (необязательно):",
        "vid_grok_task_expired": "Срок задачи этого видео истёк, его больше нельзя продлить или улучшить. Создайте новое видео.",

        "vid_grokimag_title":  "◈  <b>Grok Imagine</b>",
        "vid_grokimag_select": "  Выберите тип генерации:",
        "vid_grokimag_15":    "Grok Imagine 1.5  —  Классик",
        "vid_grokimag_t2v":   "Текст в видео",
        "vid_grokimag_i2v":   "Изображение в видео",

        "vid_extend_title": "◈  <b>Veo 3.1 — Продление видео</b>",
        "vid_extend_desc": "  Продлите ваше видео на дополнительные секунды.\n\n  Выберите тариф:",
        "vid_extend_fast":    "⚡  Быстро",
        "vid_extend_premium": "◈  Премиум",

        "vid_unknown_tool_alert": "Неизвестный инструмент",
        "vid_select_lang_label": "◈  Выберите целевой язык:",
        "vid_translate_cost": "  Стоимость   <b>{coins} монет</b>",
        "vid_send_video_any_format": "  Отправьте видеофайл в любом формате\n  (MP4, MOV, AVI, MKV и т.д.)",
        "vid_please_send_video": "Отправьте видеофайл (MP4, MOV, AVI, MKV и т.д.)\n\nВведите /cancel для отмены.",
        "vid_video_received": "✓  Видео получено",
        "vid_add_notes_prompt": "  Добавьте примечания (необязательно)\n  или пропустите и подтвердите заказ:",
        "vid_btn_add_notes": "✎  Добавить примечание",
        "vid_add_notes_only": "✎  Добавьте примечания или инструкции (необязательно):",

        "vid_attach_start_frame": "  ◈  Стартовый кадр\n",
        "vid_attach_end_frame": "  ◈  Финальный кадр\n",
        "vid_attach_imgs": "  ◈  {count} референс(ов)-изображений\n",
        "vid_attach_vids": "  ◈  {count} референс(ов)-видео\n",
        "vid_attach_auds": "  ◈  {count} аудиофайл(ов)\n",

        "vid_attach_optional_inline": "Прикрепите референс-файлы (необязательно)\n  или сразу переходите к промпту.",
        "vid_sd_attach_warning": (
            "  ⚠️  Стартовый/финальный кадр нельзя сочетать\n"
            "  с другими типами вложений."
        ),
        "vid_btn_start_frame": "Стартовый кадр",
        "vid_btn_end_frame": "Финальный кадр",
        "vid_btn_clear_startend": "✕  Очистить старт/финал",
        "vid_btn_clear": "✕  Очистить",
        "vid_btn_image_ref": "◈  Референс-изображение  ({count}/{max})",
        "vid_btn_image_reference": "◈  Референс-изображение",
        "vid_btn_image_reference_max": "◈  Референс-изображение  (до {max})",
        "vid_btn_video_ref": "◈  Референс-видео  ({count}/{max})",
        "vid_btn_video_reference": "◈  Референс-видео",
        "vid_btn_video_reference_max": "◈  Референс-видео  (до {max}){req}",
        "vid_btn_audio_file": "◈  Аудиофайл  ({count}/{max})",
        "vid_btn_audio_file_plain": "◈  Аудиофайл",
        "vid_btn_audio_file_max": "◈  Аудиофайл  (до {max})",
        "vid_btn_start_end_frame": "◈  Стартовый и финальный кадр",
        "vid_btn_start_frame_only": "◈  Стартовый кадр",
        "vid_required_label": " *обязательно",
        "vid_btn_write_prompt": "✓  Написать промпт →",
        "vid_btn_skip_write_prompt": "▸  Пропустить — написать промпт",
        "vid_btn_confirm_order": "◈  Подтвердить заказ",
        "vid_btn_upload_required": "⚠️  Загрузите {items}, чтобы продолжить",
        "vid_required_and": " и ",
        "vid_required_video": "видео",
        "vid_required_image": "изображение",
        "vid_required_audio": "аудио",
        "vid_required_start_frame": "стартовый кадр",
        "vid_required_files_alert": "Загрузите необходимые файлы: {items}",
        "vid_required_files_alert_simple": "Сначала загрузите необходимые файлы.",

        "vid_start_frame_title": "◈  <b>Стартовый кадр</b>",
        "vid_start_frame_desc": "  Отправьте изображение для <b>первого кадра</b> видео.\n\n  Указывайте его в промпте как <code>@start</code>",
        "vid_start_frame_desc_short": "  Отправьте изображение для <b>первого кадра</b>.\n\n  Указывайте его в промпте как <code>@start</code>",
        "vid_end_frame_title": "◈  <b>Финальный кадр</b>",
        "vid_end_frame_desc": "  Отправьте изображение для <b>последнего кадра</b> видео.\n\n  Указывайте его в промпте как <code>@end</code>",
        "vid_end_frame_desc_short": "  Отправьте изображение для <b>последнего кадра</b>.\n\n  Указывайте его в промпте как <code>@end</code>",
        "vid_please_send_image": "◈  Отправьте файл изображения (JPG, PNG, WEBP и т.д.)",
        "vid_please_send_video_short": "◈  Отправьте видеофайл (MP4, MOV, AVI и т.д.)",
        "vid_please_send_audio": "◈  Отправьте аудиофайл (MP3, OGG, WAV, M4A и т.д.)",
        "err_file_too_large": "⚠️  Файл слишком большой — Telegram-боты могут скачивать файлы только до 20МБ. Сожмите файл или отправьте файл меньшего размера.",
        "vid_start_frame_saved": "✓  Стартовый кадр сохранён.\n\nТеперь укажите финальный кадр или напишите промпт.",
        "vid_end_frame_saved": "✓  Финальный кадр сохранён.\n\nНапишите промпт, когда будете готовы.",

        "vid_img_ref_title": "◈  <b>Референс-изображение</b>  ({count}/{max})",
        "vid_img_ref_instructions": (
            "  Отправьте до <b>{max} изображений</b> в качестве референса.\n\n"
            "  <code>@img1</code>, <code>@img2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждое изображение\n"
            "  словами в промпте (например, «женщина на фото 1»).\n\n"
            "  Отправляйте изображения по одному или альбомом.\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "vid_img_ref_instructions_short": (
            "  Отправьте до <b>{max} изображения(ий)</b>.\n"
            "  <code>@img1</code> и т.д. — это просто метки для вас, ИИ\n"
            "  их не считывает. Опишите каждое изображение словами.\n\n"
            "  Нажмите Готово, когда закончите."
        ),
        "vid_img_max_reached": "Достигнут максимум {max} изображений. Нажмите Готово, чтобы продолжить.",
        "vid_img_max_reached_short": "Достигнут максимум {max} изображения(ий). Нажмите Готово.",
        "vid_img_saved": "✓  Изображение @img{n} сохранено.  ({count}/{max})",
        "vid_img_saved_short": "✓  @img{n} сохранено  ({count}/{max})",
        "vid_send_more_or_done": "Отправьте ещё или нажмите Готово.",
        "vid_max_reached_tap_done": "Достигнут максимум. Нажмите Готово.",

        "vid_vid_ref_title": "◈  <b>Референс-видео</b>  ({count}/{max})",
        "vid_vid_ref_instructions": (
            "  Отправьте до <b>{max} видео</b> в качестве референса.\n\n"
            "  <code>@vid1</code>, <code>@vid2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждое видео\n"
            "  словами в промпте.\n\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "vid_vid_ref_instructions_short": (
            "  Отправьте до <b>{max} видео</b> в любом формате.\n"
            "  <code>@vid1</code> и т.д. — это просто метки для вас, ИИ\n"
            "  их не считывает. Опишите каждое видео словами.\n\n"
            "  Нажмите Готово, когда закончите."
        ),
        "vid_vid_max_reached": "Достигнут максимум {max} видео. Нажмите Готово, чтобы продолжить.",
        "vid_vid_max_reached_short": "Достигнут максимум {max} видео. Нажмите Готово.",
        "vid_vid_saved": "✓  Видео @vid{n} сохранено.  ({count}/{max})",
        "vid_vid_saved_short": "✓  @vid{n} сохранено  ({count}/{max})",

        "vid_aud_ref_title": "◈  <b>Аудиофайл</b>  ({count}/{max})",
        "vid_aud_ref_instructions": (
            "  Отправьте до <b>{max} аудиофайлов</b>.\n\n"
            "  <code>@aud1</code>, <code>@aud2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждый аудиофайл\n"
            "  словами в промпте.\n\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "vid_aud_ref_instructions_short": (
            "  Отправьте до <b>{max} аудиофайла(ов)</b>.\n"
            "  <code>@aud1</code> и т.д. — это просто метки для вас, ИИ\n"
            "  их не считывает. Опишите каждый аудиофайл словами.\n\n"
            "  Нажмите Готово, когда закончите."
        ),
        "vid_aud_max_reached": "Достигнут максимум {max} аудиофайлов. Нажмите Готово, чтобы продолжить.",
        "vid_aud_max_reached_short": "Достигнут максимум {max} аудиофайла(ов). Нажмите Готово.",
        "vid_aud_saved": "✓  Аудио @aud{n} сохранено.  ({count}/{max})",
        "vid_aud_saved_short": "✓  @aud{n} сохранено  ({count}/{max})",

        "vid_attached_files_label": "\n  <b>Прикреплённые файлы:</b>\n{lines}\n  Примечание: эти метки нужны только для вас —\n  ИИ их не считывает. Опишите каждый файл словами\n  в промпте.\n",
        "vid_attach_n_imgs": "  ◈  {count} изображение(й) → @img1",
        "vid_attach_n_vids": "  ◈  {count} видео → @vid1",
        "vid_attach_n_auds": "  ◈  {count} аудио → @aud1",
        "vid_attach_start_attached": "  ◈  Стартовый кадр прикреплён\n",
        "vid_attach_end_attached": "  ◈  Финальный кадр прикреплён\n",
        "vid_now_select_resolution": "  Теперь выберите разрешение:",

        "vid_hgtr_quality_desc": (
            "  Выберите режим качества:\n\n"
            "  <b>Precision</b>  —  максимальная точность, медленнее\n"
            "  <b>Speed</b>  —  быстрее, дешевле"
        ),
        "vid_btn_precision": "◈  Precision",
        "vid_btn_speed": "◈  Speed",

        "vid_hga4_select_ar": "  Выберите соотношение сторон:",
        "vid_hga4_select_res": "  Выберите разрешение:",
        "vid_hga4_select_style": "  Выберите стиль речи:",
        "vid_omni_desc": "  Анимируйте любой портрет с озвучкой.\n\n  Выберите длительность:",

        # ── Wallet / top-up flow ────────────────────────────────
        "wallet_title": "◈  <b>Ваш кошелёк</b>",
        "wallet_balance": "  Баланс       <b>{coins} монет</b>  (≈ ${usd})",
        "wallet_rate": "  Курс           1 монета  =  $0.05",
        "wallet_min_topup": "  Мин. пополнение   $2.00  =  40 монет",
        "wallet_btn_add_coins": "＋  Пополнить",
        "wallet_btn_referral": "◈  Реферальная программа",

        "wallet_topup_title": "＋  <b>Пополнение</b>",
        "wallet_topup_rate_line": "  1 монета  =  <b>$0.05</b>",
        "wallet_topup_min_line": "  $2.00   =  <b>40 монет</b>  ← минимум",
        "wallet_topup_5_line": "  $5.00   =  <b>100 монет</b>",
        "wallet_topup_10_line": "  $10.00  =  <b>200 монет</b>",
        "wallet_topup_select_or_custom": "Выберите сумму или введите свою:",
        "wallet_btn_2": "$2  →  40 монет",
        "wallet_btn_5": "$5  →  100 монет",
        "wallet_btn_10": "$10  →  200 монет",
        "wallet_btn_20": "$20  →  400 монет",
        "wallet_btn_custom": "✎  Своя сумма",

        "wallet_custom_title": "✎  <b>Своя сумма</b>",
        "wallet_custom_desc": "Введите сумму в USD (минимум $2.00):\n\n<i>Пример: 7.5</i>",
        "wallet_min_deposit_error": "Минимальное пополнение — ${min}. Введите корректную сумму (например, 2, 5, 10).",
        "wallet_enter_number_error": "Введите число (например, 5 или 7.50).\n\nВведите /cancel для отмены.",

        "wallet_confirm_title": "◈  <b>Подтверждение пополнения</b>",
        "wallet_confirm_amount": "  Сумма        <b>${amount}</b>",
        "wallet_confirm_receive": "  Вы получите   <b>{coins} монет</b>",
        "wallet_choose_payment": "Выберите способ оплаты:",
        "wallet_btn_pay_stars": "⭐  Оплатить Stars ({stars} XTR)",
        "wallet_btn_pay_usdt": "₮  Оплатить USDT (TRC20)",

        "wallet_usdt_title": "₮  <b>Оплата USDT</b>",
        "wallet_usdt_send_exactly": "  Отправьте ровно  <b>${amount} USDT</b>",
        "wallet_usdt_network": "  Сеть              <b>TRC20 (Tron)</b>",
        "wallet_usdt_address_label": "  Адрес кошелька:",
        "wallet_usdt_after_sending": "После отправки вставьте <b>хэш транзакции</b> ниже.\n<i>Система проверит его автоматически.</i>",

        "wallet_verifying": "⏳  Проверка транзакции...",
        "wallet_verified_title": "✓  <b>Платёж подтверждён</b>",
        "wallet_verified_confirmed": "  Транзакция подтверждена",
        "wallet_verified_amount": "  Получено   <b>${amount} USDT</b>",
        "wallet_verified_coins": "  Зачислено монет   <b>{coins} монет</b>",
        "wallet_verified_balance": "  Новый баланс       <b>{coins} монет</b>",

        "wallet_review_title": "◌  <b>На проверке</b>",
        "wallet_review_body": (
            "  Не удалось автоматически проверить транзакцию.\n"
            "  Наша команда проверит её вручную в течение 15 минут.\n\n"
            "  Монеты будут зачислены после подтверждения."
        ),

        "wallet_stars_invoice_title": "RetainX Studio — Монеты",
        "wallet_stars_invoice_desc": "Пополнение на {coins} монет для аккаунта RetainX",
        "wallet_stars_label": "{coins} монет",
        "wallet_stars_success_title": "⭐  <b>Платёж успешен</b>",
        "wallet_stars_success_body": "  {coins} монет добавлено на ваш счёт.\n  Новый баланс: <b>{coins2} монет</b>",

        "wallet_topup_confirmed_title": "✓  <b>Пополнение подтверждено</b>",
        "wallet_topup_confirmed_body": "  <b>{coins} монет</b> добавлено на ваш счёт.\n  Баланс: <b>{balance} монет</b>",
        "wallet_topup_rejected": "✕  Ваше пополнение не было подтверждено. Свяжитесь с поддержкой.",

        "wallet_btn_yoomoney": "₽  Оплатить картой РФ",
        "wallet_yoomoney_title": "₽  <b>Пополнение через ЮMoney</b>",
        "wallet_yoomoney_rate_line": "  1 монета  =  <b>3.70 ₽</b>",
        "wallet_yoomoney_min_line": "  185 ₽   =  <b>50 монет</b>  ← минимум",
        "wallet_yoomoney_prompt": "Введите сумму в рублях, которую хотите оплатить:\n\n<i>Пример: 500</i>",
        "wallet_yoomoney_min_error": "Минимальная сумма — {min} ₽ (50 монет). Введите большую сумму.",
        "wallet_yoomoney_confirm_title": "₽  <b>Оплата через ЮMoney</b>",
        "wallet_yoomoney_confirm_amount": "  Сумма       <b>{amount} ₽</b>",
        "wallet_yoomoney_confirm_coins": "  Вы получите  <b>{coins} монет</b>",
        "wallet_yoomoney_confirm_note": "Нажмите кнопку ниже для оплаты. Монеты зачислятся автоматически после платежа.",
        "wallet_btn_pay_yoomoney": "₽  Оплатить {amount} ₽ картой РФ",
        "wallet_yoomoney_success_title": "✓  <b>Платёж получен</b>",
        "wallet_yoomoney_success_body": "  <b>{coins} монет</b> добавлено на ваш счёт.\n  Оплата: <b>{amount} ₽</b>",

        "wallet_btn_card": "💳  Оплата картой РФ",
        "wallet_card_title": "💳  <b>Оплата картой РФ</b>",
        "wallet_card_rate_line": "  1 монета  =  <b>3.70 ₽</b>",
        "wallet_card_min_line": "  185 ₽   =  <b>50 монет</b>  ← минимум",
        "wallet_card_prompt": "Введите сумму в рублях, которую хотите оплатить:\n\n<i>Пример: 500</i>",
        "wallet_card_min_error": "Минимальная сумма — {min} ₽ (50 монет). Введите большую сумму.",
        "wallet_card_confirm_title": "💳  <b>Оплата картой</b>",
        "wallet_card_confirm_amount": "  Сумма         <b>{amount} ₽</b>",
        "wallet_card_confirm_coins": "  Вы получите   <b>{coins} монет</b>",
        "wallet_card_number_label": "  Номер карты:",
        "wallet_card_note": "Переведите сумму на карту выше.\nЗатем отправьте <b>скриншот</b> или <b>номер чека</b> в качестве подтверждения.",
        "wallet_card_submitted_title": "⏳  <b>На проверке</b>",
        "wallet_card_submitted_body": "  Ваш платёж проверяется.\n  Монеты будут зачислены в течение 15 минут.",
        "wallet_card_success_title": "✓  <b>Платёж подтверждён</b>",
        "wallet_card_success_body": "  <b>{coins} монет</b> добавлено на ваш счёт.\n  Новый баланс: <b>{balance} монет</b>",
        "wallet_card_rejected_title": "✕  <b>Платёж не подтверждён</b>",
        "wallet_card_rejected_body": "  Ваш платёж картой не удалось подтвердить.\n  Обратитесь к @RetainXStudio.",

        "wallet_session_expired": "⚠️  Сессия истекла. Начните новое пополнение из меню кошелька.",
        "wallet_tx_already_used": "⚠️  Эта транзакция уже была использована. Используйте другую транзакцию.",

        "wallet_referral_bonus_title": "◈  <b>Реферальный бонус</b>",
        "wallet_referral_bonus_body": "  Ваш реферал совершил платёж.\n  Вам начислено <b>{bonus} ◈</b> ({percentage}%) в качестве реферального бонуса.",

        "referral_friend_joined": "👤  <b>Новый реферал!</b>\n\n  {username} перешёл по вашей ссылке.\n  Вы получите бонус когда он совершит первую покупку.",

        "wallet_referral_title": "◈  <b>Реферальная программа</b>",
        "wallet_referral_tier_line": "  ◉  <b>{name}</b>  →  {next}",
        "wallet_referral_tier_max": "  ★  <b>{name}</b>  ·  Максимальный уровень",
        "wallet_referral_rate": "  Вы получаете  <b>{first}%</b> первый платёж  ·  <b>{repeat}%</b> повторный",
        "wallet_referral_stat_invited": "Приглашено друзей",
        "wallet_referral_stat_buyers": "Совершили покупку",
        "wallet_referral_stat_balance": "Реферальный баланс",
        "wallet_referral_stat_total": "Всего заработано",
        "wallet_referral_join_bonus_note": "🎁  Каждый друг получает +{bonus} монет бонусом при регистрации!",
        "wallet_referral_share_btn": "📤  Поделиться ссылкой",
        "wallet_referral_share_text": "Использую @RetainXStudioBot для AI-генерации видео и изображений — Sora 2, Grok, Seedance, HeyGen и другие. Переходи по моей ссылке и получи +10 монет бонусом! 🎁\n",

        "wallet_referral_desc": "  Получайте <b>20%</b> с первого платежа вашего реферала\n  и <b>10%</b> с каждого последующего.\n  Начисления поступают на реферальный баланс в ₽.",
        "wallet_referral_balance_line": "  Реферальный баланс   <b>{balance} ₽</b>",
        "wallet_referral_total_line": "  Всего заработано       <b>{total} ₽</b>",
        "wallet_referral_stats_line": "  Рефералов:  <b>{count}</b>  ·  Оплатили:  <b>{buyers}</b>",
        "wallet_referral_my_list_btn": "👥  Мои рефералы ({count})",
        "wallet_referral_list_title": "👥  <b>Мои рефералы</b>",
        "wallet_referral_list_empty": "  Рефералов пока нет.\n  Поделитесь ссылкой, чтобы начать зарабатывать!",
        "wallet_referral_list_header": "  <b>Всего {count}</b>  ·  {buyers} совершили покупку",
        "wallet_referral_sub_followers": "👥 {n} подписчиков",
        "wallet_referral_sub_buyers": "🛒 {n} покупок",
        "wallet_referral_blogger_totals": "  Итого через блогеров: {sub} подписчиков  ·  {sub_buyers} покупок",
        "wallet_referral_promo_btn": "🎟  Мой промокод",

        "promo_btn": "🎟  Промокод",
        "promo_active_btn": "🎟  Промокод: {code}  (−{pct}%)",
        "promo_cancel_btn": "✕  Отменить промокод",
        "promo_enter_title": "◈  <b>Промокод</b>",
        "promo_enter_desc": "  Введите промокод и получите скидку 30%\n  на первое пополнение монет.",
        "promo_invalid": "  ✕  Промокод не найден.",
        "promo_own_code": "  ✕  Нельзя использовать свой промокод.",
        "promo_already_used": "  ✕  Вы уже использовали промокод ранее.",
        "promo_not_first": "  ✕  Промокод действует только на первое пополнение.",
        "promo_applied": "  ✓  Промокод <b>{code}</b> применён  ·  скидка <b>−{pct}%</b>",
        "promo_cancelled": "  Промокод отменён.",
        "wallet_confirm_original": "  Без скидки         <b>{amount}</b>",
        "wallet_confirm_discounted": "  К оплате             <b>{discounted}</b>  <i>(−{pct}%)</i>",
        "my_promo_title": "◈  <b>Мой промокод</b>",
        "my_promo_none": "  У вас пока нет промокода.\n  Создайте его и поделитесь с аудиторией.",
        "my_promo_create_btn": "✦  Создать промокод",
        "my_promo_code_label": "  Код           <b>{code}</b>",
        "my_promo_discount_label": "  Скидка      <b>−{pct}%</b>  ·  только первое пополнение",
        "my_promo_uses_label": "  Использований   <b>{uses}</b>",
        "my_promo_share_hint": "  Делитесь кодом в постах и видео.",

        "wallet_referral_link_label": "Ваша ссылка:",
        "wallet_referral_share": "  Поделитесь ей и зарабатывайте пассивно.",
        "wallet_referral_withdraw_btn": "₽  Вывести {amount} ₽",
        "wallet_referral_withdraw_unavailable": "◌  Мин. вывод: {min} ₽",
        "wallet_referral_withdraw_pending": "◌  Запрос на вывод обрабатывается...",
        "wallet_referral_withdraw_low_alert": "Минимальная сумма вывода — {min} ₽. Продолжайте зарабатывать!",
        "wallet_referral_withdraw_title": "₽  <b>Вывод реферального баланса</b>",
        "wallet_referral_withdraw_amount": "  Сумма к выводу   <b>{amount} ₽</b>",
        "wallet_referral_enter_requisites": "Введите номер карты или реквизиты для оплаты\n(номер карты, телефон для СБП и т.д.):",
        "wallet_referral_requisites_invalid": "Пожалуйста, введите корректные реквизиты (номер карты, телефон и т.д.).",
        "wallet_referral_withdraw_submitted_title": "✓  <b>Запрос на вывод принят</b>",
        "wallet_referral_withdraw_submitted_body": "  Сумма: <b>{amount} ₽</b>\n\n  Наша команда обработает запрос вручную в течение 24 часов.",
        "wallet_referral_withdraw_paid_title": "✓  <b>Вывод выполнен</b>",
        "wallet_referral_withdraw_paid_body": "  <b>{amount} ₽</b> отправлено на ваши реквизиты.",
        "wallet_referral_withdraw_rejected_title": "◌  <b>Вывод отклонён</b>",
        "wallet_referral_withdraw_rejected_body": "  Вывод на сумму <b>{amount} ₽</b> был отклонён.\n  Средства возвращены на реферальный баланс.\n  Свяжитесь с @RetainXStudio для уточнений.",

        # ── Order history flow ──────────────────────────────────
        "order_history_title": "◈  <b>История заказов</b>",
        "order_history_empty": "  У вас пока нет заказов.\n\n  Начните генерацию, чтобы увидеть историю здесь.",
        "order_history_total": "  Всего заказов   <b>{total}</b>",
        "order_history_completed": "  Завершено        <b>{delivered}</b>",
        "order_history_spent": "  Потрачено монет  <b>{spent}◈</b>",
        "order_history_tap_to_view": "  Нажмите на заказ, чтобы увидеть детали:",
        "order_not_found": "Заказ не найден",
        "order_detail_title": "◈  <b>Заказ #{oid}</b>",
        "order_detail_status": "  Статус    {emoji}  <b>{status}</b>",
        "order_detail_model": "  Модель     <b>{tool}</b>",
        "order_detail_coins": "  Монеты     {coins}◈",
        "order_detail_date": "  Дата          {date}",
        "order_detail_resolution": "  Разрешение    {res}",
        "order_detail_aspect_ratio": "  Соотношение сторон  {ar}",
        "order_detail_duration": "  Длительность   {dur} сек",
        "order_detail_quality": "  Качество        {quality}",
        "order_detail_audio": "  Аудио            Да",
        "order_detail_language": "  Язык             {lang}",
        "order_detail_prompt_label": "  Промпт:",
        "order_btn_repeat": "↺  Повторить заказ",
        "order_btn_back": "← Назад",
        "order_repeat_title": "◈  <b>Повтор заказа</b>",
        "order_repeat_model": "  Модель     <b>{tool}</b>",
        "order_repeat_resolution": "  Разрешение   {res}",
        "order_repeat_aspect": "  Соотношение   {ar}",
        "order_repeat_duration": "  Длительность  {dur} сек",
        "order_repeat_cost": "  Стоимость      <b>{coins} монет</b>",
        "order_repeat_prev_prompt": "  Предыдущий промпт:",
        "order_repeat_enter_prompt": "  Введите промпт (или отправьте такой же, как выше):",
        "order_status_processing": "В обработке",
        "order_status_delivered": "Доставлен",
        "order_status_cancelled": "Отменён",
        "order_your_result": "◈  Ваш результат",

        # ── Maintenance ──────────────────────────────────────────
        "maintenance_msg": "🔧 <b>Технические работы</b>\n\nБот временно недоступен. Попробуйте позже.",
        "maintenance_alert": "🔧 Технические работы. Бот временно недоступен.",

        # ── Unlimited pass UI ────────────────────────────────────
        "unlim_active_line": "\n{emoji} <b>Безлимит {name} активен</b> — осталось {mins}м {secs}с\n",
        "unlim_btn_buy": "⚡  Безлимит — купить пакет",
        "unlim_btn_active": "⚡  Безлимит {name} активен ✓",
        "unlim_active_toast": "⚡ Безлимит активен!",
        "unlim_buy_title": "⚡  <b>Безлимитные пакеты</b>",
        "unlim_buy_balance": "  Ваш баланс:  <b>{coins}◈</b>",
        "unlim_buy_select": "  Выберите тариф:",
        "unlim_btn_info": "ℹ  Подробнее о пакетах",
        "unlim_dur_1h": "1 час  —  {coins}◈",
        "unlim_dur_2h": "2 часа  —  {coins}◈  (−10%/ч)",
        "unlim_dur_3h": "3 часа  —  {coins}◈  (−20%/ч)",
        "unlim_select_duration": "  Выберите длительность:",
        "unlim_not_enough": "Недостаточно монет. Нужно {need}◈, у вас {have}◈.",
        "unlim_confirm_title": "⚡  <b>Подтверждение покупки</b>",
        "unlim_confirm_tier": "  Тариф:          <b>{name}</b>",
        "unlim_confirm_dur": "  Длительность:  <b>{hours} ч</b>",
        "unlim_confirm_cost": "  Стоимость:     <b>{cost}◈</b>",
        "unlim_confirm_balance": "  Ваш баланс:   <b>{coins}◈</b>",
        "unlim_btn_activate": "✓  Активировать — {cost}◈",
        "unlim_error_retry": "Ошибка. Попробуйте снова.",
        "unlim_no_balance": "Недостаточно монет. Пополните баланс.",
        "unlim_activated_title": "⚡  <b>Безлимит {name} активирован!</b>",
        "unlim_activated_body": "  Действует до  <b>{time}</b>  ({hours} ч)\n  Генерируйте сколько угодно!\n\n  Списано:  <b>{cost}◈</b>",
        "unlim_info_title": "⚡  <b>Безлимитные пакеты</b>",
        "unlim_info_body": "  Генерируйте неограниченно в течение\n  1, 2 или 3 часов — без списания монет\n  за каждый запрос.\n\n  Выберите пакет чтобы узнать подробнее:",
        "unlim_btn_buy_plan": "🛒  Купить {label}",
        "unlim_tier_std_info": (
            "  ✓  Seedance 2.0 Fast · Wan 2.7 · Grok 1.5\n"
            "  ✓  LTX 2.3 Pro · Veo 3.1 Lite · Kling 3.0 · Kling O3\n"
            "  ✕  Premium видео (Veo 3.1, Sora 2)\n"
            "  ✕  Аудио / войсовер\n"
            "  ✕  Аватары\n"
            "  ⬆  Разрешение до 720p"
        ),
        "unlim_tier_pro_info": (
            "  ✓  Всё из Стандарт (до 1080p)\n"
            "  ✓  Premium: Veo 3.1 · Veo 3.1 Fast · Sora 2\n"
            "  ✓  Аудио / войсовер\n"
            "  ✕  Аватары\n"
            "  ⬆  Разрешение до 1080p"
        ),
        "unlim_tier_vip_info": (
            "  ✓  Всё из Про\n"
            "  ✓  Разрешение до 4K\n"
            "  ✕  Аватары"
        ),
        "unlim_page_std": (
            "⚡  <b>Безлимит Standard</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Генерируйте видео и изображения без\n"
            "  ограничений — монеты не списываются.\n\n"
            "<b>📹 Видео — Standard:</b>\n"
            "  • Seedance 2.0 Fast\n"
            "  • Wan 2.7\n"
            "  • LTX 2.3 Pro\n"
            "  • Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5  <i>(макс. 480p)</i>\n\n"
            "<b>🎬 Видео — Kling:</b>\n"
            "  • Kling 3.0\n"
            "  • Kling O3\n\n"
            "  ✕  Premium видео (Veo 3.1, Sora 2)\n"
            "  ✕  Аудио и голос\n"
            "  ✕  Аватары\n\n"
            "  ⬆  Разрешение: до 720p\n\n"
            "<b>💰 Стоимость:</b>\n"
            "  1 час   →  <b>{p1}◈</b>\n"
            "  2 часа  →  <b>{p2}◈</b>  <i>(−10% за час)</i>\n"
            "  3 часа  →  <b>{p3}◈</b>  <i>(−20% за час)</i>"
        ),
        "unlim_page_pro": (
            "⚡⚡  <b>Безлимит Pro</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Всё из Standard плюс Premium-модели\n"
            "  и аудио — в качестве до 1080p.\n\n"
            "<b>📹 Видео — Standard (до 1080p):</b>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • LTX 2.3 Pro · Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5\n\n"
            "<b>🎬 Видео — Kling (до 1080p):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 Premium видео (до 1080p):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 Аудио и голос:</b>\n"
            "  • ElevenLabs · Artlist и др.\n\n"
            "  ✕  Аватары\n\n"
            "  ⬆  Разрешение: до 1080p\n\n"
            "<b>💰 Стоимость:</b>\n"
            "  1 час   →  <b>{p1}◈</b>\n"
            "  2 часа  →  <b>{p2}◈</b>  <i>(−10% за час)</i>\n"
            "  3 часа  →  <b>{p3}◈</b>  <i>(−20% за час)</i>"
        ),
        "unlim_page_vip": (
            "♛  <b>Безлимит VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  Максимальный пакет — всё из Pro\n"
            "  с разрешением до 4K.\n\n"
            "  ✓  Все модели из Pro\n\n"
            "<b>📹 Standard-видео (до 4K):</b>\n"
            "  • LTX 2.3 Pro  <i>(720p / 1080p / 2K / 4K)</i>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • Veo 3.1 Lite · Grok Imagine 1.5\n\n"
            "<b>🎬 Kling (до 4K):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 Premium видео (до 4K):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 Аудио и голос</b>\n\n"
            "  ✕  Аватары\n\n"
            "  ⬆  Разрешение: до 4K\n\n"
            "<b>💰 Стоимость:</b>\n"
            "  1 час   →  <b>{p1}◈</b>\n"
            "  2 часа  →  <b>{p2}◈</b>  <i>(−10% за час)</i>\n"
            "  3 часа  →  <b>{p3}◈</b>  <i>(−20% за час)</i>"
        ),
        "unlim_tier_title": "⚡  <b>Безлимит {name}</b>",
        "unlim_info_tier_btn": "{emoji}  {name}  —  от {coins}◈",
    },
    "ar": {
        "welcome_title": "◈  <b>مرحباً بك في RetainX Studio</b>",
        "welcome_body": (
            "  أسرع وأوفر طريقة\n"
            "  لإنشاء فيديو وصور وصوت بالذكاء الاصطناعي.\n\n"
            "  ◉  Kling 3.0  ·  Veo 3.1  ·  Sora 2\n"
            "  ◉  Midjourney  ·  Flux  ·  Seedance\n"
            "  ◉  HeyGen  ·  ElevenLabs  ·  LTX\n\n"
            "  أرخص بـ <b>3 أضعاف</b> من أي منافس.\n"
            "  النتائج خلال <b>~دقيقتين.</b>"
        ),
        "welcome_bonus": "  🎁  أُضيف <b>{bonus} عملة</b> إلى حسابك.\n  الرصيد   <b>{coins} عملة</b>",
        "what_create": "ماذا تريد أن تنشئ؟",
        "choose_option": "اختر خياراً:",

        "main_menu_title": "◈  <b>RetainX Studio</b>",
        "main_menu_balance": "  الرصيد   <b>{coins} عملة</b>",
        "main_menu_desc": "  إنشاء فيديو وصور وصوت بالذكاء الاصطناعي\n  بأنسب الأسعار.",
        "maintenance_banner": "⚠️  <b>أعمال الصيانة: 10 – 13 يوليو</b>\n      قد يكون البوت غير متاح مؤقتاً.\n",

        "btn_video_generation": "▸  إنشاء الفيديو",
        "btn_image_generation": "▸  إنشاء الصور",
        "btn_audio_voice": "▸  الصوت",
        "btn_wallet_coins": "◈  المحفظة  ·  {coins} عملة",
        "btn_pricing": "◎  الأسعار",
        "btn_support": "◌  الدعم",
        "btn_language": "◐  اللغة",
        "btn_start_generating": "▸  ابدأ الإنشاء",
        "btn_view_pricing": "◎  عرض الأسعار",
        "btn_back": "←  رجوع",
        "btn_help": "📖  المساعدة",

        # ── Help pages ──
        "help_main_text": (
            "📖  <b>المساعدة — RetainX Studio</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  اختر قسماً للحصول على معلومات تفصيلية:"
        ),
        "help_start_text": (
            "🚀  <b>كيف تبدأ</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>نظام العملات</b>\n"
            "  1 عملة = $0.05   ·   $1 = 20 عملة\n"
            "  الحد الأدنى للشحن: $2 (40 عملة)\n\n"
            "  <b>الخطوات الأولى</b>\n"
            "  1 · اختر النوع — فيديو، صورة أو صوت\n"
            "  2 · اختر النموذج والإعدادات\n"
            "  3 · أدخل البرومبت بأي لغة\n"
            "  4 · احصل على النتيجة خلال ~2 دقيقة\n\n"
            "  <b>مكافأة الترحيب</b>\n"
            "  20 عملة مجانية عند أول تشغيل 🎁\n\n"
            "  <b>أكواد الترويج</b>\n"
            "  استخدم /promo [الكود] للتفعيل\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_video_text": (
            "🎬  <b>توليد الفيديو</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>القياسية</b>  (متاحة للجميع)\n"
            "  Seedance 2.0 Fast · Wan 2.7 · LTX 2.3 Pro\n"
            "  Veo 3.1 Lite · Grok 1.5\n\n"
            "  <b>Kling</b>  (متاحة للجميع)\n"
            "  Kling 3.0 · Kling O3  ·  حتى 4K\n\n"
            "  <b>المميزة</b>  (Pro / VIP غير محدود)\n"
            "  Veo 3.1 Full · Veo 3.1 Fast · Sora 2 Pro\n\n"
            "  <b>الأفاتار والدبلجة</b>\n"
            "  HeyGen · ElevenLabs · Lipsync · OmniHuman\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "  اضغط على قسم للتفاصيل ↓"
        ),
        "help_vid_std_text": (
            "▸  <b>نماذج الفيديو القياسية</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Seedance 2.0 Fast</b>\n"
            "  480p / 720p  ·  4–15 ثانية\n"
            "  من 5◈ (480p 4ث)  إلى 45◈ (720p 15ث)\n\n"
            "<b>Wan 2.7</b>\n"
            "  720p / 1080p  ·  2–15 ثانية\n"
            "  من 4◈ (720p 2ث)  إلى 45◈ (1080p 15ث)\n\n"
            "<b>LTX 2.3 Pro</b>\n"
            "  720p / 1080p / 2K / 4K  ·  6–10 ثانية\n"
            "  من 6◈ (720p)  إلى 75◈ (4K 10ث)\n\n"
            "<b>Veo 3.1 Lite</b>\n"
            "  720p / 1080p  ·  4–8 ثانية\n"
            "  من 3◈ (720p 4ث)  إلى 8◈ (1080p 8ث)\n\n"
            "<b>Grok 1.5</b>\n"
            "  حتى 15 ثانية  ·  4◈/ث  (60◈ لـ15ث)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_prem_text": (
            "★  <b>نماذج الفيديو المميزة</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "  ⚠️ يتطلب خطة غير محدودة Pro / VIP\n\n"
            "<b>Veo 3.1 Full</b>  (أفضل جودة Google)\n"
            "  720p / 1080p / 4K  ·  4–8 ثانية\n"
            "  من 15◈ (720p 4ث)  إلى 58◈ (4K 8ث)\n\n"
            "<b>Veo 3.1 Fast</b>\n"
            "  720p / 1080p / 4K  ·  4–8 ثانية\n"
            "  من 8◈ (720p 4ث)  إلى 40◈ (4K 8ث)\n\n"
            "<b>Sora 2 Pro</b>  (OpenAI)\n"
            "  720p / 1080p  ·  4–12 ثانية\n"
            "  من 26◈ (720p 4ث)  إلى 114◈ (1080p 12ث)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_kling_text": (
            "◉  <b>نماذج Kling للفيديو</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Kling 3.0</b>\n"
            "  720p / 1080p / 4K  ·  3–15 ثانية\n"
            "  من 4◈ (720p 3ث)  إلى 75◈ (4K 15ث)\n\n"
            "<b>Kling O3</b>  (جودة فائقة)\n"
            "  720p / 1080p / 4K  ·  3–15 ثانية\n"
            "  من 4◈ (720p 3ث)  إلى 75◈ (4K 15ث)\n\n"
            "  ✓ اتباع دقيق للبرومبت\n"
            "  ✓ مشاهد فوتوغرافية واقعية\n"
            "  ✓ دعم صور المرجع\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_vid_avatar_text": (
            "◌  <b>الأفاتار والدبلجة</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>HeyGen Avatar</b>\n"
            "  720p / 1080p  ·  1–15 دقيقة  ·  60◈/دقيقة\n\n"
            "<b>ElevenLabs Dubbing</b>\n"
            "  دبلجة احترافية  ·  60◈/دقيقة\n"
            "  29 لغة مدعومة\n\n"
            "<b>Lipsync</b>\n"
            "  مزامنة الشفاه مع الصوت  ·  60◈/دقيقة\n\n"
            "<b>OmniHuman / Aurora Avatar</b>\n"
            "  أفاتار من صورة + صوت\n"
            "  60◈/دقيقة (OmniHuman)  ·  54◈/دقيقة (Aurora)\n\n"
            "  الصيغ: MP4, MOV, AVI\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_images_text": (
            "🖼  <b>توليد الصور</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>Nano Banana Pro</b>   1K–2K: 3◈  ·  4K: 4◈\n"
            "  <b>Nano Banana 2</b>     1K–2K: 2◈  ·  4K: 3◈\n"
            "  <b>Seedream 5.0 Pro</b>  1K: 1◈  ·  2K: 2◈\n"
            "  <b>GPT Image 2</b>       1K: 1◈  ·  2K: 2◈  ·  4K: 3◈\n"
            "  <b>Wan 2.7 Pro</b>       4K: 2◈\n"
            "  <b>Flux 2.0 Pro</b>      1K–2K: 1◈\n"
            "  <b>Ideogram v3</b>       Turbo/Balanced: 1◈  ·  Quality: 2◈\n"
            "  <b>Topaz Upscaler</b>    2K: 2◈  ·  4K: 3◈  ·  8K: 6◈\n\n"
            "  الصيغ: 1:1 · 16:9 · 9:16 · 3:4 وأكثر\n"
            "  صور المرجع: حتى 14 صورة\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_audio_text": (
            "🔊  <b>الصوت والتعليق</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>ElevenLabs Voiceover</b>\n"
            "  تحويل النص إلى كلام احترافي بالذكاء الاصطناعي\n\n"
            "  ✓ أكثر من 1000 صوت\n"
            "  ✓ التحكم في المشاعر وأسلوب الكلام\n"
            "  ✓ ضبط استقرار الصوت\n"
            "  ✓ تأثيرات صوتية\n"
            "  ✓ التحكم في سرعة الكلام\n"
            "  ✓ أكثر من 30 لغة\n\n"
            "  متاح مع خطة غير محدودة Pro / VIP\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_text": (
            "◈  <b>المحفظة والدفع</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  رصيدك محفوظ بعملات RetainX.\n"
            "  تُخصم العملات تلقائياً\n"
            "  عند كل عملية توليد.\n\n"
            "  اختر قسماً للتفاصيل:"
        ),
        "help_wallet_rates_text": (
            "◎  <b>الأسعار والحدود</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>سعر العملة</b>\n"
            "  1 عملة = $0.05\n"
            "  $1 = 20 عملة\n\n"
            "  <b>حدود الشحن</b>\n"
            "  الحد الأدنى:    $2.00 = 40 عملة\n"
            "  عبر Stars:      40 عملة على الأقل\n"
            "  عبر USDT:       $2 على الأقل\n\n"
            "  <b>طرق الدفع</b>\n"
            "  ⭐ Telegram Stars\n"
            "  ₮ USDT (TRC-20)\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_stars_text": (
            "⭐  <b>الشحن عبر Telegram Stars</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>كيفية الشحن:</b>\n"
            "  1 · اضغط «◈ المحفظة» في القائمة الرئيسية\n"
            "  2 · اضغط «＋ إضافة عملات»\n"
            "  3 · اختر «⭐ Stars»\n"
            "  4 · أدخل عدد العملات (40 كحد أدنى)\n"
            "  5 · ادفع عبر Telegram — بدون مغادرة التطبيق\n\n"
            "  يُحسب سعر Stars تلقائياً.\n\n"
            "  ✓ إضافة فورية\n"
            "  ✓ لا حاجة لبطاقة أو محفظة تشفير\n"
            "  ✓ آمن — مدمج في Telegram\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_wallet_usdt_text": (
            "₮  <b>الشحن عبر USDT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  الشبكة: TRC-20 (Tron)\n\n"
            "  <b>كيفية الشحن:</b>\n"
            "  1 · اضغط «◈ المحفظة» → «＋ إضافة»\n"
            "  2 · اختر «₮ USDT»\n"
            "  3 · أدخل المبلغ بالدولار (حد أدنى $2)\n"
            "  4 · أرسل USDT إلى العنوان المعروض\n"
            "  5 · أخبر المشغّل بعد الدفع\n\n"
            "  ✓ نقبل USDT TRC-20\n"
            "  ✓ الإضافة خلال 15 دقيقة\n"
            "  ✓ لا عمولة من البوت\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_text": (
            "⚡  <b>الخطط غير المحدودة</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  تزيل الخطة غير المحدودة جميع القيود\n"
            "  وتفتح نماذج إضافية.\n\n"
            "  الخطة نشطة لمدة 1 أو 2 أو 3 ساعات —\n"
            "  أنشئ بلا حدود خلال هذا الوقت.\n\n"
            "  <b>الخطط:</b>\n"
            "  ⚡  Standard  —  من 268◈/ساعة\n"
            "  ⚡⚡  Pro       —  من 662◈/ساعة\n"
            "  ♛   VIP       —  من 1619◈/ساعة\n\n"
            "  اضغط على خطة للتفاصيل ↓\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_std_text": (
            "⚡  <b>غير محدود Standard</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>الأسعار:</b>\n"
            "  1 س  —  268◈\n"
            "  2 س  —  482◈  (توفير 10%)\n"
            "  3 س  —  642◈  (توفير 20%)\n\n"
            "  <b>النماذج المتاحة:</b>\n"
            "  ✓ Seedance 2.0 Fast  ·  Wan 2.7\n"
            "  ✓ LTX 2.3 Pro  ·  Veo 3.1 Lite\n"
            "  ✓ Grok 1.5\n"
            "  ✓ Kling 3.0  ·  Kling O3\n\n"
            "  <b>أقصى دقة:</b>  720p\n\n"
            "  ✕ النماذج المميزة (Veo Full, Sora)\n"
            "  ✕ الأفاتار والدبلجة\n"
            "  ✕ توليد الصوت\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_pro_text": (
            "⚡⚡  <b>غير محدود Pro</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>الأسعار:</b>\n"
            "  1 س  —  662◈\n"
            "  2 س  —  1192◈  (توفير 10%)\n"
            "  3 س  —  1589◈  (توفير 20%)\n\n"
            "  <b>النماذج المتاحة:</b>\n"
            "  ✓ جميع نماذج Standard\n"
            "  ✓ Veo 3.1 Full  ·  Veo 3.1 Fast\n"
            "  ✓ Sora 2 Pro\n"
            "  ✓ Kling 3.0  ·  Kling O3\n"
            "  ✓ ElevenLabs Voiceover (صوت)\n\n"
            "  <b>أقصى دقة:</b>  1080p\n\n"
            "  ✕ الأفاتار والدبلجة\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_unlim_vip_text": (
            "♛  <b>غير محدود VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  <b>الأسعار:</b>\n"
            "  1 س  —  1619◈\n"
            "  2 س  —  2914◈  (توفير 10%)\n"
            "  3 س  —  3886◈  (توفير 20%)\n\n"
            "  <b>النماذج المتاحة:</b>\n"
            "  ✓ جميع نماذج Standard و Pro\n"
            "  ✓ Veo 3.1 Full  ·  Sora 2 Pro\n"
            "  ✓ Kling 3.0  ·  Kling O3\n"
            "  ✓ ElevenLabs Voiceover (صوت)\n\n"
            "  <b>أقصى دقة:</b>  4K\n\n"
            "  ✓ وصول كامل لجميع الميزات\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_ref_text": (
            "👥  <b>برنامج الإحالة</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  شارك رابطك → يسجّل الصديق ويشحن\n"
            "  → تحصل على % من كل عملية شحن.\n\n"
            "  <b>مستويات المكافآت:</b>\n"
            "  Starter (0–5 إحالات)\n"
            "    أول شحن  20%  ·  متكرر  10%\n\n"
            "  Partner (6–15 إحالة)\n"
            "    أول شحن  22%  ·  متكرر  12%\n\n"
            "  Pro (16+ إحالة)\n"
            "    أول شحن  25%  ·  متكرر  15%\n\n"
            "  <b>أكواد الترويج للمدوّنين</b>\n"
            "  تعمل كرابط الإحالة.\n"
            "  يدخل المستخدم الجديد /promo الكود.\n\n"
            "  رابطك: ◈ المحفظة → برنامج الإحالة\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "help_support_text": (
            "💬  <b>الدعم</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  هل لديك سؤال أو مشكلة؟\n"
            "  اكتب لنا مباشرةً:\n\n"
            "  @RetainXStudio\n\n"
            "  <b>وقت الرد:</b>  عادةً خلال ساعة\n\n"
            "  <b>نساعدك في:</b>\n"
            "  ✓ عدم استلام الفيديو / الصورة\n"
            "  ✓ خصم عملات غير صحيح\n"
            "  ✓ مشاكل الشحن\n"
            "  ✓ أخطاء تقنية\n"
            "  ✓ أسئلة حول النماذج\n\n"
            "  للأكواد الترويجية والشراكات —\n"
            "  تواصل أيضاً عبر @RetainXStudio\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        # ── Help button labels ──
        "help_btn_start":       "🚀  كيف تبدأ",
        "help_btn_video":       "🎬  توليد الفيديو",
        "help_btn_vid_std":     "▸  النماذج القياسية",
        "help_btn_vid_prem":    "★  النماذج المميزة",
        "help_btn_vid_kling":   "◉  Kling",
        "help_btn_vid_avatar":  "◌  الأفاتار والدبلجة",
        "help_btn_images":      "🖼  توليد الصور",
        "help_btn_audio":       "🔊  الصوت والتعليق",
        "help_btn_wallet":      "◈  المحفظة والدفع",
        "help_btn_wallet_rates":"◎  الأسعار والحدود",
        "help_btn_wallet_stars":"⭐  Telegram Stars",
        "help_btn_wallet_usdt": "₮  USDT / تشفير",
        "help_btn_unlim":       "⚡  الخطط غير المحدودة",
        "help_btn_unlim_std":   "⚡  Standard",
        "help_btn_unlim_pro":   "⚡⚡  Pro",
        "help_btn_unlim_vip":   "♛  VIP",
        "help_btn_ref":         "👥  برنامج الإحالة",
        "help_btn_support":     "💬  الدعم",

        "audio_title": "◌  <b>الصوت</b>",
        "audio_body": "  قريباً.\n\n  نحن نعمل على دمج أدوات\n  تركيب الصوت وتوليد الموسيقى.\n\n  ترقّب التحديثات.",
        "audio_pro_vip_body": "  الصوت متاح في خطط البرو والـ VIP\n  غير المحدودة.\n\n  قم بالترقية للوصول إلى\n  تركيب الصوت وتوليد الصوت.",
        "audio_unlimited_only": "  توليد الصوت متاح ضمن\n  <b>اشتراك Unlimited</b>.\n\n  اشترك في خطة Unlimited للوصول إلى\n  التعليق الصوتي بالذكاء الاصطناعي\n  مع الكتالوج الكامل للأصوات.",

        "tts_coin_menu_body":   "  أنشئ أصواتاً بالذكاء الاصطناعي باستخدام عملاتك.\n  اختر نموذج TTS:",
        "tts_select_voice":     "اختر صوتاً:",
        "tts_page_indicator":   "صفحة {page}/{total}",
        "tts_voice_card_prompt":"  استمع للمعاينة، ثم اختر هذا الصوت.",
        "tts_btn_preview":      "🎵  معاينة",
        "tts_btn_choose":       "✓  اختر هذا الصوت",
        "tts_enter_text_prompt":"  أدخل النص لتحويله إلى كلام.\n  الحد الأقصى {max} حرفاً.",
        "tts_text_too_long":    "  النص طويل جداً (الحد الأقصى {max} حرفاً).\n  يرجى اختصاره والمحاولة مرة أخرى.",
        "tts_order_summary_title": "◈  <b>ملخص الطلب</b>",
        "tts_voice_label":      "  الصوت:   <b>{name}</b>",
        "tts_model_label":      "  النموذج: {model}",
        "tts_cost_label":       "  التكلفة: ",
        "tts_balance_label":    "  الرصيد:  ",
        "tts_text_label":       "  النص:",
        "tts_confirm_btn":      "توليد ({coins}◈)",
        "tts_edit_text_btn":    "تعديل النص",
        "tts_order_placed_title": "◈  <b>تم تقديم الطلب #{oid}</b>",
        "tts_voice_row":        "  الصوت    <b>{name}</b>",
        "tts_coins_deducted":   "  تم خصم {coins}◈ من رصيدك",
        "tts_estimated_delivery":"  تقديراً: ~{minutes} دقيقة",
        "tts_will_deliver":     "  سيُرسَل الصوت هنا عند الاكتمال.",
        "tts_session_expired":  "انتهت الجلسة، يرجى البدء من جديد.",
        "tts_insufficient_coins":"رصيد غير كافٍ. يرجى إعادة الشحن.",

        "vid_subcat_tier_alert": "هذه الفئة غير مشمولة في خطتك الحالية.",

        "vo_low_balance_notice": "رصيد منخفض: {coins} عملة — أضف رصيداً قبل الطلب.",
        "vo_select_model": "  اختر نموذج الذكاء الاصطناعي للصوت:",
        "vo_select_category": "  اختر فئة الصوت:",
        "vo_select_gender": "  اختر جنس الصوت:",
        "vo_select_age": "  اختر عمر الصوت:",
        "vo_select_voice": "  اختر صوتاً:",
        "vo_btn_listen_all": "🔊  استمع للجميع ({count})",
        "vo_listen_all_sending": "🔊 جارٍ الإرسال…",
        "vo_select_language": "  اختر اللغة:",
        "vo_preview_error": "⚠️  فشل تحميل المعاينة. يرجى المحاولة مرة أخرى.",
        "vo_voice_gender_label": "  الجنس      {gender}",
        "vo_voice_age_label": "  العمر       {age}",
        "vo_voice_category_label": "  الفئة        {category}",
        "vo_voice_model_label": "  النموذج     {model}",
        "vo_voice_language_label": "  اللغة         {language}",
        "vo_btn_choose_voice": "✓  استخدم هذا الصوت",
        "vo_btn_listen": "🎧  استمع للعينة",
        "vo_btn_change_language": "🌐  تغيير اللغة  ·  {language}",
        "vo_preview_caption": "🎧  {voice}  —  {language}  ({model})",
        "vo_voice_stability_label": "  الثبات   {pct}%",
        "vo_voice_effect_label": "  التأثير    {effect}",
        "vo_btn_stability": "🎚  الثبات  ·  {pct}%",
        "vo_select_stability": "  اضبط ثبات الصوت.\n  الأقل يعني أكثر تعبيراً، والأكثر يعني أكثر ثباتاً.",
        "vo_btn_effect": "🎭  التأثير  ·  {effect}",
        "vo_select_effect": "  اختر تأثير الصوت:",
        "vo_effect_preview_caption": "🎭  {effect}  —  عينة التأثير",
        "vo_btn_done": "✓  تم",
        "vo_stability_label": "  الثبات   <b>{pct}%</b>",
        "vo_effect_label": "  التأثير    <b>{effect}</b>",
        "vo_voice_emotion_label": "  المشاعر   {emotion}",
        "vo_btn_emotion": "🙂  المشاعر  ·  {emotion}",
        "vo_select_emotion": "  اختر المشاعر:",
        "vo_emotion_label": "  المشاعر     <b>{emotion}</b>",
        "vo_voice_speed_label": "  السرعة   {speed}x",
        "vo_btn_speed": "⏱  السرعة  ·  {speed}x",
        "vo_select_speed": "  اضبط سرعة الكلام.",
        "vo_speed_label": "  السرعة     <b>{speed}x</b>",
        "vo_enter_text": "  أدخل النص الذي تريد من هذا الصوت قراءته:",
        "vo_edit_text_prompt": "  أدخل النص الجديد لهذا الصوت:",
        "vo_order_summary_title": "◈  <b>ملخص طلب التعليق الصوتي</b>",
        "vo_voice_label": "  الصوت       <b>{name}</b>",
        "vo_model_label": "  النموذج      <b>{model}</b>",
        "vo_language_label": "  اللغة          <b>{language}</b>",
        "vo_text_label": "  النص",
        "vo_cost_label": "  التكلفة   ",
        "vo_balance_label": "  الرصيد    ",
        "vo_btn_confirm": "✓  تأكيد  ·  {coins} عملة",
        "vo_btn_edit_text": "✎  تعديل النص",
        "vo_session_expired": "انتهت الجلسة، يرجى البدء من جديد.",
        "vo_insufficient_coins": "رصيد غير كافٍ. يرجى شحن المحفظة.",
        "vo_order_placed_title": "✓  <b>تم تقديم طلب التعليق الصوتي #{oid}!</b>",
        "vo_voice_row": "  الصوت       <b>{name}</b>",
        "vo_coins_deducted": "  العملات المخصومة   <b>{coins} عملة</b>",
        "vo_estimated_delivery": "  وقت التسليم المتوقع: ~{minutes} دقيقة",
        "vo_will_deliver": "  سنرسل ملف الصوت مباشرةً في هذه المحادثة.",

        "support_title": "◌  <b>الدعم</b>",
        "support_body": "  تواصل معنا: @RetainXStudio",

        "video_title": "◈  <b>إنشاء الفيديو</b>",
        "select_category": "اختر فئة:",

        "images_title": "◈  <b>إنشاء الصور</b>",
        "select_model": "اختر نموذجاً:",

        "pricing_title": "◎  <b>الأسعار</b>",
        "pricing_body": "  1 عملة  =  <b>$0.05</b>\n\n  اختر فئة لعرض الأسعار:",
        "btn_image_pricing": "▸  أسعار الصور",
        "btn_video_pricing": "▸  أسعار الفيديو",

        "price_images_title": "◎  <b>أسعار الصور</b>",
        "price_video_title": "◎  <b>أسعار الفيديو</b>",
        "price_video_body": (
            "  تتفاوت الأسعار حسب النموذج والدقة والمدة.\n"
            "  اختر نموذجاً في قسم إنشاء الفيديو\n"
            "  لرؤية التكلفة الدقيقة بالعملات.\n\n"
            "  <b>أسعار نموذجية:</b>\n"
            "  Kling 3.0   720p  5s  —  6◈\n"
            "  Veo 3.1     4K    8s  —  58◈\n"
            "  Seedance   1080p 10s  —  60◈\n"
        ),

        "menu_main_menu": "⌂  القائمة الرئيسية",
        "menu_wallet": "◈  المحفظة",
        "menu_video": "▸  فيديو",
        "menu_images": "▸  صور",
        "menu_audio": "▸  صوت",
        "menu_orders": "≡  الطلبات",
        "menu_support": "◌  الدعم",

        "lang_title": "◐  <b>اللغة</b>",
        "lang_desc": "  اختر لغتك المفضلة:",
        "lang_changed": "✓  تم تحديث اللغة.",

        "coins_word": "عملة",

        # ── Image generation flow ──────────────────────────────
        "img_menu_title": "◈  <b>إنشاء الصور</b>",
        "img_menu_select": "اختر نموذجاً للمتابعة:",
        "img_price_label": "السعر",
        "img_per_gen": "لكل توليد",
        "img_select_ar": "اختر نسبة الأبعاد:",
        "img_select_quality": "اختر الجودة:",
        "img_aspect_ratio_label": "نسبة الأبعاد",
        "img_quality_label": "الجودة",
        "img_cost_label": "التكلفة",
        "img_balance_label": "رصيدك",
        "img_attach_optional": "  أرفق صور مرجعية (اختياري)\n  أو تخطَّ لكتابة البروم بت.",
        "img_btn_add_ref": "◈  إضافة صورة مرجعية  (حتى {max})",
        "img_btn_skip_prompt": "▸  تخطّ — اكتب البروم بت",
        "img_enter_prompt": "أدخل البروم بت:",
        "img_order_summary_title": "◈  <b>ملخص الطلب</b>",
        "img_model_label": "النموذج",
        "img_prompt_label": "البروم بت:",
        "img_btn_confirm": "◈  تأكيد  ({coins} عملة)",
        "img_btn_confirm_free": "◈  تأكيد  (مجاني)",
        "img_btn_edit_prompt": "✎  تعديل البروم بت",
        "img_edit_prompt_prompt": "✎  أدخل البروم بت الجديد:",
        "img_session_expired": "انتهت الجلسة. يرجى بدء طلبك من جديد.",
        "img_insufficient_coins": "رصيد غير كافٍ. يرجى شحن المحفظة.",
        "img_order_error": "⚠️  فشل تقديم الطلب. تم استرداد عملاتك.",
        "img_order_placed_title": "◌  <b>تم تقديم الطلب #{oid}</b>",
        "img_model_row": "  النموذج     <b>{name}</b>",
        "img_coins_deducted": "  العملات      <b>{coins} مخصومة</b>",
        "img_estimated_time": "  الوقت المتوقع  ~{minutes} دقيقة",
        "img_will_deliver": "  سنرسل صورتك هنا قريباً.",
        "img_ref_title": "◈  <b>صورة مرجعية</b>  ({count}/{max})",
        "img_ref_instructions": (
            "  أرسل حتى <b>{max} صور</b> كمرجع.\n\n"
            "  <code>@img1</code>، <code>@img2</code> إلخ مجرد تسميات\n"
            "  لك — الذكاء الاصطناعي لا يقرأها. صف كل صورة\n"
            "  بالكلمات في البروم بت.\n\n"
            "  اضغط <b>تم</b> عند الانتهاء."
        ),
        "btn_done": "✓  تم",
        "img_ref_saved": "✓  تم حفظ الصورة @img{n}.  ({count}/{max})",
        "img_ref_send_more": "أرسل المزيد أو اضغط تم.",
        "img_ref_max_reached": "تم الوصول للحد الأقصى. اضغط تم.",
        "img_ref_max_alert": "تم الوصول للحد الأقصى {max} صورة. اضغط تم للمتابعة.",
        "img_ref_required_alert": "يرجى إرفاق صورة قبل المتابعة.",
        "img_refs_attached": "  ◈  {count} صورة مرجعية مرفقة\n",

        # ── Video generation flow ──────────────────────────────
        "vid_menu_title": "◈  <b>إنشاء الفيديو</b>",
        "vid_select_category": "اختر فئة:",
        "vid_low_balance_notice": "رصيد منخفض: {coins} عملة — أضف رصيداً قبل الطلب.",
        "vid_sub_standard": "▸  فيديو قياسي",
        "vid_sub_grok": "▸  Grok فيديو",
        "vid_sub_premium": "▸  فيديو مميز",
        "vid_sub_kling": "▸  Kling فيديو",
        "vid_sub_avatar": "▸  الأفاتار والدبلجة",
        "vid_select_model": "اختر نموذجاً:",
        "vid_unknown_tool": "الأداة غير موجودة",
        "vid_resolution_word": "الدقة",
        "vid_duration_word": "المدة",
        "vid_sec_word": "ثانية",
        "vid_type_word": "النوع",
        "vid_avatar_video_word": "فيديو الأفاتار",
        "vid_select_resolution": "  اختر الدقة:",
        "vid_select_aspect_ratio": "  اختر نسبة الأبعاد:",
        "vid_select_duration": "  اختر المدة:",
        "vid_resolution_label": "  الدقة    {res}",
        "vid_aspect_ratio_label": "  نسبة الأبعاد  {ar}",
        "vid_duration_label": "  المدة       {dur} ثانية",
        "vid_cost_label": "  التكلفة       <b>{coins} عملة</b>",
        "vid_cost_label_short": "  التكلفة   <b>{coins} عملة</b>",
        "vid_balance_label": "  الرصيد        {coins} عملة",
        "vid_audio_label": "  الصوت      {audio}",
        "vid_audio_yes": "نعم",
        "vid_audio_no": "لا",
        "vid_include_audio": "  هل تريد تضمين الصوت في الفيديو؟",
        "vid_btn_with_audio": "🔊  مع الصوت",
        "vid_btn_no_audio": "🔇  بدون صوت",
        "vid_enter_prompt": "أدخل البروم بت:",
        "vid_btn_confirm": "◈  تأكيد  ({coins} عملة)",
        "vid_btn_edit_prompt": "✎  تعديل البروم بت",
        "vid_edit_prompt_prompt": "✎  أدخل البروم بت الجديد:",
        "vid_order_summary_title": "◈  <b>ملخص الطلب</b>",
        "vid_model_label": "  النموذج       <b>{name}</b>",
        "vid_language_label": "  اللغة           {lang}",
        "vid_attachments_label": "\n  المرفقات:\n",
        "vid_prompt_label": "  البروم بت:",
        "vid_session_expired": "انتهت الجلسة. يرجى بدء طلبك من جديد.",
        "vid_insufficient_coins": "رصيد غير كافٍ. يرجى شحن المحفظة.",
        "vid_avatar_blocked_unlimited": "أدوات الأفاتار غير متاحة خلال اشتراك Unlimited.",
        "vid_order_error": "⚠️  فشل تقديم الطلب. تم استرداد عملاتك.",
        "vid_order_placed_title": "◌  <b>تم تقديم الطلب #{oid}</b>",
        "vid_model_row": "  النموذج     <b>{name}</b>",
        "vid_coins_deducted": "  العملات      <b>{coins} مخصومة</b>",
        "vid_estimated_delivery": "  وقت التسليم المتوقع  ~{minutes} دقيقة",
        "vid_will_deliver": "  سيتم إرسال نتيجتك هنا.",
        "order_ready_caption": (
            "◈  <b>طلبك جاهز</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  الطلب     #{oid}\n"
            "  النموذج   {tool}\n\n"
            "  شكراً لاختيارك RetainX Studio."
        ),

        "vid_grok_title": "◈  <b>Grok Imagine 1.5</b>",
        "vid_grok_resolution_line": "  الدقة: 720p\n\n  اختر المدة:",
        "vid_grok_res_select": "  الدقة: {res}\n\n  اختر المدة:",
        "vid_grokt_title": "◈  <b>Grok نص إلى فيديو</b>",
        "vid_groki_title": "◈  <b>Grok صورة إلى فيديو</b>",
        "vid_btn_char_photo":   "صورة الشخصية",
        "vid_char_photo_title": "◈  <b>صورة الشخصية</b>",
        "vid_char_photo_desc":  "  أرسل صورة الشخصية التي تريد تحريكها.\n\n  سيولّد النموذج حركة مستوحاة من هذه الصورة.",
        "vid_grok_mode_select": "  اختر وضع التوليد:",
        "vid_grok_mode_fun": "مرح",
        "vid_grok_mode_normal": "عادي",
        "vid_grok_mode_spicy": "مثير",
        "vid_grok_extend_prompt": "◈  <b>Grok Extend  +{secs}ث</b>\n━━━━━━━━━━━━━━━━━━━━\n\n  أدخل وصفاً لتوجيه التمديد (اختياري):",
        "vid_grok_task_expired": "انتهت صلاحية مهمة هذا الفيديو ولا يمكن تمديده أو تحسينه. يرجى إنشاء فيديو جديد.",

        "vid_grokimag_title":  "◈  <b>Grok Imagine</b>",
        "vid_grokimag_select": "  اختر نوع التوليد:",
        "vid_grokimag_15":    "Grok Imagine 1.5  —  الكلاسيكي",
        "vid_grokimag_t2v":   "نص إلى فيديو",
        "vid_grokimag_i2v":   "صورة إلى فيديو",

        "vid_extend_title": "◈  <b>Veo 3.1 — تمديد الفيديو</b>",
        "vid_extend_desc": "  مدّد الفيديو بثوانٍ إضافية.\n\n  اختر المستوى:",
        "vid_extend_fast":    "⚡  سريع",
        "vid_extend_premium": "◈  بريميوم",

        "vid_unknown_tool_alert": "أداة غير معروفة",
        "vid_select_lang_label": "◈  اختر اللغة المستهدفة:",
        "vid_translate_cost": "  التكلفة   <b>{coins} عملة</b>",
        "vid_send_video_any_format": "  أرسل ملف الفيديو بأي صيغة\n  (MP4, MOV, AVI, MKV إلخ)",
        "vid_please_send_video": "يرجى إرسال ملف فيديو (MP4, MOV, AVI, MKV إلخ)\n\nاكتب /cancel للإلغاء.",
        "vid_video_received": "✓  تم استقبال الفيديو",
        "vid_add_notes_prompt": "  أضف ملاحظات إضافية (اختياري)\n  أو تخطَّ لتأكيد الطلب:",
        "vid_btn_add_notes": "✎  إضافة ملاحظة",
        "vid_add_notes_only": "✎  أضف ملاحظات أو تعليمات (اختياري):",

        "vid_attach_start_frame": "  ◈  الإطار الأول\n",
        "vid_attach_end_frame": "  ◈  الإطار الأخير\n",
        "vid_attach_imgs": "  ◈  {count} صورة مرجعية\n",
        "vid_attach_vids": "  ◈  {count} فيديو مرجعي\n",
        "vid_attach_auds": "  ◈  {count} ملف صوتي\n",

        "vid_attach_optional_inline": "أرفق ملفات مرجعية (اختياري)\n  أو انتقل مباشرةً إلى البروم بت.",
        "vid_sd_attach_warning": (
            "  ⚠️  لا يمكن الجمع بين الإطار الأول/الأخير\n"
            "  وأنواع المرفقات الأخرى."
        ),
        "vid_btn_start_frame": "الإطار الأول",
        "vid_btn_end_frame": "الإطار الأخير",
        "vid_btn_clear_startend": "✕  مسح الأول/الأخير",
        "vid_btn_clear": "✕  مسح",
        "vid_btn_image_ref": "◈  صورة مرجعية  ({count}/{max})",
        "vid_btn_image_reference": "◈  صورة مرجعية",
        "vid_btn_image_reference_max": "◈  صورة مرجعية  (حتى {max})",
        "vid_btn_video_ref": "◈  فيديو مرجعي  ({count}/{max})",
        "vid_btn_video_reference": "◈  فيديو مرجعي",
        "vid_btn_video_reference_max": "◈  فيديو مرجعي  (حتى {max}){req}",
        "vid_btn_audio_file": "◈  ملف صوتي  ({count}/{max})",
        "vid_btn_audio_file_plain": "◈  ملف صوتي",
        "vid_btn_audio_file_max": "◈  ملف صوتي  (حتى {max})",
        "vid_btn_start_end_frame": "◈  الإطار الأول والأخير",
        "vid_btn_start_frame_only": "◈  الإطار الأول",
        "vid_required_label": " *مطلوب",
        "vid_btn_write_prompt": "✓  اكتب البروم بت →",
        "vid_btn_skip_write_prompt": "▸  تخطّ — اكتب البروم بت",
        "vid_btn_confirm_order": "◈  تأكيد الطلب",
        "vid_btn_upload_required": "⚠️  ارفع {items} للمتابعة",
        "vid_required_and": " و ",
        "vid_required_video": "فيديو",
        "vid_required_image": "صورة",
        "vid_required_audio": "صوت",
        "vid_required_start_frame": "الإطار الأول",
        "vid_required_files_alert": "يرجى رفع الملفات المطلوبة: {items}",
        "vid_required_files_alert_simple": "يرجى رفع الملفات المطلوبة أولاً.",

        "vid_start_frame_title": "◈  <b>الإطار الأول</b>",
        "vid_start_frame_desc": "  أرسل الصورة للإطار الأول <b>لفيديوك</b>.\n\n  أشر إليه في البروم بت بـ <code>@start</code>",
        "vid_start_frame_desc_short": "  أرسل الصورة للإطار الأول.\n\n  أشر إليه في البروم بت بـ <code>@start</code>",
        "vid_end_frame_title": "◈  <b>الإطار الأخير</b>",
        "vid_end_frame_desc": "  أرسل الصورة للإطار الأخير <b>لفيديوك</b>.\n\n  أشر إليه في البروم بت بـ <code>@end</code>",
        "vid_end_frame_desc_short": "  أرسل الصورة للإطار الأخير.\n\n  أشر إليه في البروم بت بـ <code>@end</code>",
        "vid_please_send_image": "◈  يرجى إرسال ملف صورة (JPG, PNG, WEBP إلخ)",
        "vid_please_send_video_short": "◈  يرجى إرسال ملف فيديو (MP4, MOV, AVI إلخ)",
        "vid_please_send_audio": "◈  يرجى إرسال ملف صوتي (MP3, OGG, WAV, M4A إلخ)",
        "err_file_too_large": "⚠️  الملف كبير جداً — لا تستطيع بوتات Telegram تنزيل ملفات أكبر من 20 ميجابايت. يرجى ضغط الملف أو إرسال ملف أصغر.",
        "vid_start_frame_saved": "✓  تم حفظ الإطار الأول.\n\nاختر الإطار الأخير أو اكتب البروم بت.",
        "vid_end_frame_saved": "✓  تم حفظ الإطار الأخير.\n\nاكتب البروم بت عندما تكون جاهزاً.",

        "vid_img_ref_title": "◈  <b>صورة مرجعية</b>  ({count}/{max})",
        "vid_img_ref_instructions": (
            "  أرسل حتى <b>{max} صور</b> كمرجع.\n\n"
            "  <code>@img1</code>، <code>@img2</code> إلخ مجرد تسميات\n"
            "  لك — الذكاء الاصطناعي لا يقرأها. صف كل صورة\n"
            "  بالكلمات في البروم بت (مثلاً \"المرأة في الصورة 1\").\n\n"
            "  أرسل الصور واحدة تلو الأخرى أو كألبوم.\n"
            "  اضغط <b>تم</b> عند الانتهاء."
        ),
        "vid_img_ref_instructions_short": (
            "  أرسل حتى <b>{max} صورة</b>.\n"
            "  <code>@img1</code> إلخ مجرد تسميات لك — الذكاء الاصطناعي\n"
            "  لا يقرأها. صف كل صورة بالكلمات.\n\n"
            "  اضغط تم عند الانتهاء."
        ),
        "vid_img_max_reached": "تم الوصول للحد الأقصى {max} صورة. اضغط تم للمتابعة.",
        "vid_img_max_reached_short": "تم الوصول للحد الأقصى {max} صورة. اضغط تم.",
        "vid_img_saved": "✓  تم حفظ الصورة @img{n}.  ({count}/{max})",
        "vid_img_saved_short": "✓  @img{n} محفوظة  ({count}/{max})",
        "vid_send_more_or_done": "أرسل المزيد أو اضغط تم.",
        "vid_max_reached_tap_done": "تم الوصول للحد الأقصى. اضغط تم.",

        "vid_vid_ref_title": "◈  <b>فيديو مرجعي</b>  ({count}/{max})",
        "vid_vid_ref_instructions": (
            "  أرسل حتى <b>{max} فيديوهات</b> كمرجع.\n\n"
            "  <code>@vid1</code>، <code>@vid2</code> إلخ مجرد تسميات\n"
            "  لك — الذكاء الاصطناعي لا يقرأها. صف كل فيديو\n"
            "  بالكلمات في البروم بت.\n\n"
            "  اضغط <b>تم</b> عند الانتهاء."
        ),
        "vid_vid_ref_instructions_short": (
            "  أرسل حتى <b>{max} فيديو</b> بأي صيغة.\n"
            "  <code>@vid1</code> إلخ مجرد تسميات لك — الذكاء الاصطناعي\n"
            "  لا يقرأها. صف كل فيديو بالكلمات.\n\n"
            "  اضغط تم عند الانتهاء."
        ),
        "vid_vid_max_reached": "تم الوصول للحد الأقصى {max} فيديو. اضغط تم للمتابعة.",
        "vid_vid_max_reached_short": "تم الوصول للحد الأقصى {max} فيديو. اضغط تم.",
        "vid_vid_saved": "✓  تم حفظ الفيديو @vid{n}.  ({count}/{max})",
        "vid_vid_saved_short": "✓  @vid{n} محفوظ  ({count}/{max})",

        "vid_aud_ref_title": "◈  <b>ملف صوتي</b>  ({count}/{max})",
        "vid_aud_ref_instructions": (
            "  أرسل حتى <b>{max} ملفات صوتية</b>.\n\n"
            "  <code>@aud1</code>، <code>@aud2</code> إلخ مجرد تسميات\n"
            "  لك — الذكاء الاصطناعي لا يقرأها. صف كل ملف صوتي\n"
            "  بالكلمات في البروم بت.\n\n"
            "  اضغط <b>تم</b> عند الانتهاء."
        ),
        "vid_aud_ref_instructions_short": (
            "  أرسل حتى <b>{max} ملف صوتي</b>.\n"
            "  <code>@aud1</code> إلخ مجرد تسميات لك — الذكاء الاصطناعي\n"
            "  لا يقرأها. صف كل ملف صوتي بالكلمات.\n\n"
            "  اضغط تم عند الانتهاء."
        ),
        "vid_aud_max_reached": "تم الوصول للحد الأقصى {max} ملف صوتي. اضغط تم للمتابعة.",
        "vid_aud_max_reached_short": "تم الوصول للحد الأقصى {max} ملف صوتي. اضغط تم.",
        "vid_aud_saved": "✓  تم حفظ الصوت @aud{n}.  ({count}/{max})",
        "vid_aud_saved_short": "✓  @aud{n} محفوظ  ({count}/{max})",

        "vid_attached_files_label": "\n  <b>الملفات المرفقة:</b>\n{lines}\n  ملاحظة: هذه التسميات لأغراضك الشخصية فقط —\n  الذكاء الاصطناعي لا يقرأها. صف كل ملف بالكلمات\n  في البروم بت.\n",
        "vid_attach_n_imgs": "  ◈  {count} صورة → @img1",
        "vid_attach_n_vids": "  ◈  {count} فيديو → @vid1",
        "vid_attach_n_auds": "  ◈  {count} صوت → @aud1",
        "vid_attach_start_attached": "  ◈  الإطار الأول مرفق\n",
        "vid_attach_end_attached": "  ◈  الإطار الأخير مرفق\n",
        "vid_now_select_resolution": "  اختر الدقة الآن:",

        "vid_hgtr_quality_desc": (
            "  اختر وضع الجودة:\n\n"
            "  <b>Precision</b>  —  أعلى دقة، أبطأ\n"
            "  <b>Speed</b>  —  أسرع معالجة، تكلفة أقل"
        ),
        "vid_btn_precision": "◈  Precision",
        "vid_btn_speed": "◈  Speed",

        "vid_hga4_select_ar": "  اختر نسبة الأبعاد:",
        "vid_hga4_select_res": "  اختر الدقة:",
        "vid_hga4_select_style": "  اختر أسلوب الكلام:",
        "vid_omni_desc": "  حرّك أي صورة شخصية مع صوت.\n\n  اختر المدة:",

        # ── Wallet / top-up flow ────────────────────────────────
        "wallet_title": "◈  <b>محفظتك</b>",
        "wallet_balance": "  الرصيد     <b>{coins} عملة</b>  (≈ ${usd})",
        "wallet_rate": "  السعر        1 عملة  =  $0.05",
        "wallet_min_topup": "  الحد الأدنى للشحن   $2.00  =  40 عملة",
        "wallet_btn_add_coins": "＋  إضافة عملات",
        "wallet_btn_referral": "◈  برنامج الإحالة",

        "wallet_topup_title": "＋  <b>إضافة عملات</b>",
        "wallet_topup_rate_line": "  1 عملة  =  <b>$0.05</b>",
        "wallet_topup_min_line": "  $2.00   =  <b>40 عملة</b>  ← الحد الأدنى",
        "wallet_topup_5_line": "  $5.00   =  <b>100 عملة</b>",
        "wallet_topup_10_line": "  $10.00  =  <b>200 عملة</b>",
        "wallet_topup_select_or_custom": "اختر مبلغاً أو أدخل مبلغاً مخصصاً:",
        "wallet_btn_2": "$2  →  40 عملة",
        "wallet_btn_5": "$5  →  100 عملة",
        "wallet_btn_10": "$10  →  200 عملة",
        "wallet_btn_20": "$20  →  400 عملة",
        "wallet_btn_custom": "✎  مبلغ مخصص",

        "wallet_custom_title": "✎  <b>مبلغ مخصص</b>",
        "wallet_custom_desc": "اكتب المبلغ بالدولار (الحد الأدنى $2.00):\n\n<i>مثال: 7.5</i>",
        "wallet_min_deposit_error": "الحد الأدنى للإيداع هو ${min}. يرجى إدخال مبلغ صحيح (مثلاً 2، 5، 10).",
        "wallet_enter_number_error": "يرجى إدخال رقم (مثلاً 5 أو 7.50).\n\nاكتب /cancel للإلغاء.",

        "wallet_confirm_title": "◈  <b>تأكيد الشحن</b>",
        "wallet_confirm_amount": "  المبلغ      <b>${amount}</b>",
        "wallet_confirm_receive": "  ستحصل على   <b>{coins} عملة</b>",
        "wallet_choose_payment": "اختر طريقة الدفع:",
        "wallet_btn_pay_stars": "⭐  الدفع بـ Stars ({stars} XTR)",
        "wallet_btn_pay_usdt": "₮  الدفع بـ USDT (TRC20)",

        "wallet_usdt_title": "₮  <b>الدفع بـ USDT</b>",
        "wallet_usdt_send_exactly": "  أرسل بالضبط  <b>${amount} USDT</b>",
        "wallet_usdt_network": "  الشبكة          <b>TRC20 (Tron)</b>",
        "wallet_usdt_address_label": "  عنوان المحفظة:",
        "wallet_usdt_after_sending": "بعد الإرسال، الصق <b>رقم المعاملة</b> أدناه.\n<i>سيتم التحقق منه تلقائياً.</i>",

        "wallet_verifying": "⏳  جارٍ التحقق من المعاملة...",
        "wallet_verified_title": "✓  <b>تم تأكيد الدفع</b>",
        "wallet_verified_confirmed": "  تم تأكيد المعاملة",
        "wallet_verified_amount": "  المبلغ المستلم   <b>${amount} USDT</b>",
        "wallet_verified_coins": "  العملات المُضافة     <b>{coins} عملة</b>",
        "wallet_verified_balance": "  الرصيد الجديد        <b>{coins} عملة</b>",

        "wallet_review_title": "◌  <b>قيد المراجعة</b>",
        "wallet_review_body": (
            "  لم نتمكن من التحقق من معاملتك تلقائياً.\n"
            "  سيراجعها فريقنا يدوياً خلال 15 دقيقة.\n\n"
            "  ستُضاف العملات بعد التأكيد."
        ),

        "wallet_stars_invoice_title": "RetainX Studio — عملات",
        "wallet_stars_invoice_desc": "شحن {coins} عملة إلى حسابك في RetainX",
        "wallet_stars_label": "{coins} عملة",
        "wallet_stars_success_title": "⭐  <b>تم الدفع بنجاح</b>",
        "wallet_stars_success_body": "  أُضيف {coins} عملة إلى محفظتك.\n  الرصيد الجديد: <b>{coins2} عملة</b>",

        "wallet_topup_confirmed_title": "✓  <b>تم تأكيد الشحن</b>",
        "wallet_topup_confirmed_body": "  أُضيف <b>{coins} عملة</b> إلى حسابك.\n  الرصيد: <b>{balance} عملة</b>",
        "wallet_topup_rejected": "✕  لم يتم تأكيد شحنك. يرجى التواصل مع الدعم.",

        "wallet_btn_yoomoney": "₽  الدفع بالبطاقة الروسية",
        "wallet_yoomoney_title": "₽  <b>شحن عبر YooMoney</b>",
        "wallet_yoomoney_rate_line": "  1 عملة  =  <b>3.70 ₽</b>",
        "wallet_yoomoney_min_line": "  185 ₽   =  <b>50 عملة</b>  ← الحد الأدنى",
        "wallet_yoomoney_prompt": "أدخل المبلغ بالروبل الذي تريد دفعه:\n\n<i>مثال: 500</i>",
        "wallet_yoomoney_min_error": "الحد الأدنى للإيداع {min} ₽ (50 عملة). يرجى إدخال مبلغ أكبر.",
        "wallet_yoomoney_confirm_title": "₽  <b>الدفع عبر YooMoney</b>",
        "wallet_yoomoney_confirm_amount": "  المبلغ      <b>{amount} ₽</b>",
        "wallet_yoomoney_confirm_coins": "  ستحصل على  <b>{coins} عملة</b>",
        "wallet_yoomoney_confirm_note": "اضغط الزر أدناه للدفع. تُضاف العملات تلقائياً بعد الدفع.",
        "wallet_btn_pay_yoomoney": "₽  ادفع {amount} ₽ بالبطاقة الروسية",
        "wallet_yoomoney_success_title": "✓  <b>تم استلام الدفع</b>",
        "wallet_yoomoney_success_body": "  أُضيف <b>{coins} عملة</b> إلى حسابك.\n  الدفع: <b>{amount} ₽</b>",

        "wallet_btn_card": "💳  الدفع بالبطاقة الروسية",
        "wallet_card_title": "💳  <b>الدفع بالبطاقة الروسية</b>",
        "wallet_card_rate_line": "  1 عملة  =  <b>3.70 ₽</b>",
        "wallet_card_min_line": "  185 ₽   =  <b>50 عملة</b>  ← الحد الأدنى",
        "wallet_card_prompt": "أدخل المبلغ بالروبل الذي تريد دفعه:\n\n<i>مثال: 500</i>",
        "wallet_card_min_error": "الحد الأدنى للإيداع هو {min} ₽ (50 عملة). أدخل مبلغاً أكبر.",
        "wallet_card_confirm_title": "💳  <b>الدفع بالبطاقة</b>",
        "wallet_card_confirm_amount": "  المبلغ         <b>{amount} ₽</b>",
        "wallet_card_confirm_coins": "  ستحصل على   <b>{coins} عملة</b>",
        "wallet_card_number_label": "  رقم البطاقة:",
        "wallet_card_note": "حوّل المبلغ إلى البطاقة أعلاه.\nثم أرسل <b>لقطة شاشة</b> أو <b>رقم الإيصال</b> كتأكيد.",
        "wallet_card_submitted_title": "⏳  <b>قيد المراجعة</b>",
        "wallet_card_submitted_body": "  جارٍ مراجعة دفعتك.\n  ستُضاف العملات خلال 15 دقيقة.",
        "wallet_card_success_title": "✓  <b>تم تأكيد الدفع</b>",
        "wallet_card_success_body": "  أُضيف <b>{coins} عملة</b> إلى حسابك.\n  الرصيد الجديد: <b>{balance} عملة</b>",
        "wallet_card_rejected_title": "✕  <b>لم يتم تأكيد الدفع</b>",
        "wallet_card_rejected_body": "  تعذّر تأكيد دفعتك بالبطاقة.\n  يرجى التواصل مع @RetainXStudio.",

        "wallet_session_expired": "⚠️  انتهت الجلسة. يرجى بدء عملية شحن جديدة من قائمة المحفظة.",
        "wallet_tx_already_used": "⚠️  تم استخدام هذه المعاملة من قبل. يرجى استخدام معاملة مختلفة.",

        "wallet_referral_bonus_title": "◈  <b>مكافأة الإحالة</b>",
        "wallet_referral_bonus_body": "  قام المُحال منك بدفعة.\n  حصلت على <b>{bonus} ◈</b> ({percentage}%) كمكافأة إحالة.",

        "referral_friend_joined": "👤  <b>إحالة جديدة!</b>\n\n  {username} انضم عبر رابطك.\n  ستحصل على مكافأة عند أول عملية شراء له.",

        "wallet_referral_title": "◈  <b>برنامج الإحالة</b>",
        "wallet_referral_tier_line": "  ◉  <b>{name}</b>  →  {next}",
        "wallet_referral_tier_max": "  ★  <b>{name}</b>  ·  المستوى الأقصى",
        "wallet_referral_rate": "  تكسب  <b>{first}%</b> أول دفعة  ·  <b>{repeat}%</b> للدفعات التالية",
        "wallet_referral_stat_invited": "أصدقاء مدعوون",
        "wallet_referral_stat_buyers": "أجروا عملية شراء",
        "wallet_referral_stat_balance": "رصيد الإحالة",
        "wallet_referral_stat_total": "إجمالي الأرباح",
        "wallet_referral_join_bonus_note": "🎁  كل صديق يحصل على +{bonus} عملة عند الانضمام!",
        "wallet_referral_share_btn": "📤  شارك رابطي",
        "wallet_referral_share_text": "أستخدم @RetainXStudioBot لتوليد الفيديو والصور بالذكاء الاصطناعي — Sora 2، Grok، Seedance، HeyGen والمزيد. انضم عبر رابطي واحصل على +10 عملات بونص! 🎁\n",

        "wallet_referral_desc": "  اكسب <b>20%</b> من أول دفعة لمُحالك\n  و<b>10%</b> من كل دفعة لاحقة.\n  الأرباح تُضاف إلى رصيد الإحالة بالروبل.",
        "wallet_referral_balance_line": "  رصيد الإحالة   <b>{balance} ₽</b>",
        "wallet_referral_total_line": "  إجمالي الأرباح     <b>{total} ₽</b>",
        "wallet_referral_stats_line": "  الإحالات:  <b>{count}</b>  ·  الدافعون:  <b>{buyers}</b>",
        "wallet_referral_my_list_btn": "👥  إحالاتي ({count})",
        "wallet_referral_list_title": "👥  <b>إحالاتي</b>",
        "wallet_referral_list_empty": "  لا توجد إحالات بعد.\n  شارك رابطك للبدء في الكسب!",
        "wallet_referral_list_header": "  <b>{count} إجمالاً</b>  ·  {buyers} أجروا شراءً",
        "wallet_referral_sub_followers": "👥 {n} متابع",
        "wallet_referral_sub_buyers": "🛒 {n} عملية شراء",
        "wallet_referral_blogger_totals": "  إجمالي عبر البلوغرز: {sub} متابع  ·  {sub_buyers} عملية شراء",
        "wallet_referral_promo_btn": "🎟  رمز الخصم الخاص بي",

        "promo_btn": "🎟  رمز الخصم",
        "promo_active_btn": "🎟  الرمز: {code}  (−{pct}%)",
        "promo_cancel_btn": "✕  إلغاء رمز الخصم",
        "promo_enter_title": "◈  <b>رمز الخصم</b>",
        "promo_enter_desc": "  أدخل رمز الخصم للحصول على تخفيض 30%\n  على أول شحن للعملات.",
        "promo_invalid": "  ✕  رمز الخصم غير موجود.",
        "promo_own_code": "  ✕  لا يمكنك استخدام رمزك الخاص.",
        "promo_already_used": "  ✕  لقد استخدمت رمز خصم مسبقاً.",
        "promo_not_first": "  ✕  رمز الخصم صالح للشحن الأول فقط.",
        "promo_applied": "  ✓  تم تطبيق الرمز <b>{code}</b>  ·  خصم <b>−{pct}%</b>",
        "promo_cancelled": "  تم إلغاء رمز الخصم.",
        "wallet_confirm_original": "  بدون خصم          <b>{amount}</b>",
        "wallet_confirm_discounted": "  المبلغ المدفوع      <b>{discounted}</b>  <i>(−{pct}%)</i>",
        "my_promo_title": "◈  <b>رمز الخصم الخاص بي</b>",
        "my_promo_none": "  ليس لديك رمز خصم بعد.\n  أنشئ واحداً وشاركه مع جمهورك.",
        "my_promo_create_btn": "✦  إنشاء رمز خصم",
        "my_promo_code_label": "  الرمز        <b>{code}</b>",
        "my_promo_discount_label": "  الخصم       <b>−{pct}%</b>  ·  الشحن الأول فقط",
        "my_promo_uses_label": "  الاستخدامات   <b>{uses}</b>",
        "my_promo_share_hint": "  شارك الرمز في منشوراتك ومقاطع الفيديو.",

        "wallet_referral_link_label": "رابطك:",
        "wallet_referral_share": "  شاركه واكسب بشكل سلبي.",
        "wallet_referral_withdraw_btn": "₽  سحب {amount} ₽",
        "wallet_referral_withdraw_unavailable": "◌  الحد الأدنى للسحب: {min} ₽",
        "wallet_referral_withdraw_pending": "◌  جارٍ معالجة طلب السحب...",
        "wallet_referral_withdraw_low_alert": "الحد الأدنى للسحب هو {min} ₽. استمر في الكسب!",
        "wallet_referral_withdraw_title": "₽  <b>سحب رصيد الإحالة</b>",
        "wallet_referral_withdraw_amount": "  المبلغ المراد سحبه   <b>{amount} ₽</b>",
        "wallet_referral_enter_requisites": "أدخل رقم بطاقتك البنكية أو بيانات الدفع\n(رقم البطاقة، هاتف SBP، إلخ):",
        "wallet_referral_requisites_invalid": "يرجى إدخال بيانات دفع صحيحة (رقم بطاقة، هاتف، إلخ).",
        "wallet_referral_withdraw_submitted_title": "✓  <b>تم تقديم طلب السحب</b>",
        "wallet_referral_withdraw_submitted_body": "  المبلغ: <b>{amount} ₽</b>\n\n  سيعالج فريقنا الطلب يدوياً خلال 24 ساعة.",
        "wallet_referral_withdraw_paid_title": "✓  <b>تمت معالجة السحب</b>",
        "wallet_referral_withdraw_paid_body": "  تم إرسال <b>{amount} ₽</b> إلى بيانات الدفع الخاصة بك.",
        "wallet_referral_withdraw_rejected_title": "◌  <b>تم رفض السحب</b>",
        "wallet_referral_withdraw_rejected_body": "  تم رفض سحبك بمبلغ <b>{amount} ₽</b>.\n  تم إعادة المبلغ إلى رصيد إحالتك.\n  تواصل مع @RetainXStudio للتفاصيل.",

        # ── Order history flow ──────────────────────────────────
        "order_history_title": "◈  <b>سجل الطلبات</b>",
        "order_history_empty": "  لا توجد طلبات بعد.\n\n  ابدأ بالإنشاء لترى سجلك هنا.",
        "order_history_total": "  إجمالي الطلبات   <b>{total}</b>",
        "order_history_completed": "  المكتملة          <b>{delivered}</b>",
        "order_history_spent": "  العملات المُنفقة  <b>{spent}◈</b>",
        "order_history_tap_to_view": "  اضغط على أي طلب لعرض تفاصيله:",
        "order_not_found": "الطلب غير موجود",
        "order_detail_title": "◈  <b>الطلب #{oid}</b>",
        "order_detail_status": "  الحالة    {emoji}  <b>{status}</b>",
        "order_detail_model": "  النموذج     <b>{tool}</b>",
        "order_detail_coins": "  العملات     {coins}◈",
        "order_detail_date": "  التاريخ      {date}",
        "order_detail_resolution": "  الدقة          {res}",
        "order_detail_aspect_ratio": "  نسبة الأبعاد  {ar}",
        "order_detail_duration": "  المدة          {dur} ثانية",
        "order_detail_quality": "  الجودة         {quality}",
        "order_detail_audio": "  الصوت           نعم",
        "order_detail_language": "  اللغة           {lang}",
        "order_detail_prompt_label": "  البروم بت:",
        "order_btn_repeat": "↺  تكرار الطلب",
        "order_btn_back": "← رجوع",
        "order_repeat_title": "◈  <b>تكرار الطلب</b>",
        "order_repeat_model": "  النموذج     <b>{tool}</b>",
        "order_repeat_resolution": "  الدقة         {res}",
        "order_repeat_aspect": "  نسبة الأبعاد  {ar}",
        "order_repeat_duration": "  المدة         {dur} ثانية",
        "order_repeat_cost": "  التكلفة        <b>{coins} عملة</b>",
        "order_repeat_prev_prompt": "  البروم بت السابق:",
        "order_repeat_enter_prompt": "  أدخل البروم بت (أو أرسل نفس البروم بت أعلاه):",
        "order_status_processing": "قيد المعالجة",
        "order_status_delivered": "مُسلَّم",
        "order_status_cancelled": "ملغى",
        "order_your_result": "◈  نتيجتك",

        # ── Maintenance ──────────────────────────────────────────
        "maintenance_msg": "🔧 <b>صيانة</b>\n\nالبوت غير متاح مؤقتاً. يرجى المحاولة لاحقاً.",
        "maintenance_alert": "🔧 الصيانة. البوت غير متاح مؤقتاً.",

        # ── Unlimited pass UI ────────────────────────────────────
        "unlim_active_line": "\n{emoji} <b>اشتراك {name} لا محدود نشط</b> — {mins}د {secs}ث متبقية\n",
        "unlim_btn_buy": "⚡  لا محدود — شراء خطة",
        "unlim_btn_active": "⚡  لا محدود {name} نشط ✓",
        "unlim_active_toast": "⚡ الاشتراك اللامحدود نشط!",
        "unlim_buy_title": "⚡  <b>خطط لا محدود</b>",
        "unlim_buy_balance": "  رصيدك:  <b>{coins}◈</b>",
        "unlim_buy_select": "  اختر خطة:",
        "unlim_btn_info": "ℹ  تفاصيل الخطط",
        "unlim_dur_1h": "ساعة  —  {coins}◈",
        "unlim_dur_2h": "ساعتان  —  {coins}◈  (−10%/س)",
        "unlim_dur_3h": "3 ساعات  —  {coins}◈  (−20%/س)",
        "unlim_select_duration": "  اختر المدة:",
        "unlim_not_enough": "عملات غير كافية. تحتاج {need}◈، لديك {have}◈.",
        "unlim_confirm_title": "⚡  <b>تأكيد الشراء</b>",
        "unlim_confirm_tier": "  الخطة:      <b>{name}</b>",
        "unlim_confirm_dur": "  المدة:         <b>{hours} س</b>",
        "unlim_confirm_cost": "  التكلفة:      <b>{cost}◈</b>",
        "unlim_confirm_balance": "  رصيدك:      <b>{coins}◈</b>",
        "unlim_btn_activate": "✓  تفعيل — {cost}◈",
        "unlim_error_retry": "خطأ. يرجى المحاولة مجدداً.",
        "unlim_no_balance": "عملات غير كافية. أعد شحن رصيدك.",
        "unlim_activated_title": "⚡  <b>اشتراك {name} اللامحدود مُفعَّل!</b>",
        "unlim_activated_body": "  نشط حتى  <b>{time}</b>  ({hours} س)\n  أنشئ بلا حدود!\n\n  المُخصوم:  <b>{cost}◈</b>",
        "unlim_info_title": "⚡  <b>خطط لا محدود</b>",
        "unlim_info_body": "  أنشئ بلا حدود لمدة 1 أو 2 أو 3 ساعات —\n  بدون خصم عملات لكل طلب.\n\n  اختر خطة لمعرفة التفاصيل:",
        "unlim_btn_buy_plan": "🛒  شراء {label}",
        "unlim_tier_std_info": (
            "  ✓  Seedance 2.0 Fast · Wan 2.7 · Grok 1.5\n"
            "  ✓  LTX 2.3 Pro · Veo 3.1 Lite · Kling 3.0 · Kling O3\n"
            "  ✕  فيديو بريميوم (Veo 3.1، Sora 2)\n"
            "  ✕  صوت / تعليق صوتي\n"
            "  ✕  الصور الرمزية\n"
            "  ⬆  دقة حتى 720p"
        ),
        "unlim_tier_pro_info": (
            "  ✓  كل شيء من Standard (حتى 1080p)\n"
            "  ✓  بريميوم: Veo 3.1 · Veo 3.1 Fast · Sora 2\n"
            "  ✓  صوت / تعليق صوتي\n"
            "  ✕  الصور الرمزية\n"
            "  ⬆  دقة حتى 1080p"
        ),
        "unlim_tier_vip_info": (
            "  ✓  كل شيء من Pro\n"
            "  ✓  دقة حتى 4K\n"
            "  ✕  الصور الرمزية"
        ),
        "unlim_page_std": (
            "⚡  <b>Standard لا محدود</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  أنشئ فيديوهات وصوراً بلا حدود\n"
            "  — بدون خصم عملات لكل طلب.\n\n"
            "<b>📹 فيديو — Standard:</b>\n"
            "  • Seedance 2.0 Fast\n"
            "  • Wan 2.7\n"
            "  • LTX 2.3 Pro\n"
            "  • Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5  <i>(حد أقصى 480p)</i>\n\n"
            "<b>🎬 فيديو — Kling:</b>\n"
            "  • Kling 3.0\n"
            "  • Kling O3\n\n"
            "  ✕  فيديو بريميوم (Veo 3.1، Sora 2)\n"
            "  ✕  صوت\n"
            "  ✕  الصور الرمزية\n\n"
            "  ⬆  الدقة: حتى 720p\n\n"
            "<b>💰 التسعير:</b>\n"
            "  ساعة   →  <b>{p1}◈</b>\n"
            "  ساعتان  →  <b>{p2}◈</b>  <i>(−10% في الساعة)</i>\n"
            "  3 ساعات  →  <b>{p3}◈</b>  <i>(−20% في الساعة)</i>"
        ),
        "unlim_page_pro": (
            "⚡⚡  <b>Pro لا محدود</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  كل شيء من Standard بالإضافة إلى نماذج\n"
            "  بريميوم وصوت — حتى 1080p.\n\n"
            "<b>📹 فيديو — Standard (حتى 1080p):</b>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • LTX 2.3 Pro · Veo 3.1 Lite\n"
            "  • Grok Imagine 1.5\n\n"
            "<b>🎬 فيديو — Kling (حتى 1080p):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 فيديو بريميوم (حتى 1080p):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 صوت:</b>\n"
            "  • ElevenLabs · Artlist وغيرها\n\n"
            "  ✕  الصور الرمزية\n\n"
            "  ⬆  الدقة: حتى 1080p\n\n"
            "<b>💰 التسعير:</b>\n"
            "  ساعة   →  <b>{p1}◈</b>\n"
            "  ساعتان  →  <b>{p2}◈</b>  <i>(−10% في الساعة)</i>\n"
            "  3 ساعات  →  <b>{p3}◈</b>  <i>(−20% في الساعة)</i>"
        ),
        "unlim_page_vip": (
            "♛  <b>VIP لا محدود</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "  الخطة القصوى — كل شيء من Pro\n"
            "  بدقة حتى 4K.\n\n"
            "  ✓  جميع نماذج Pro\n\n"
            "<b>📹 فيديو Standard (حتى 4K):</b>\n"
            "  • LTX 2.3 Pro  <i>(720p / 1080p / 2K / 4K)</i>\n"
            "  • Seedance 2.0 Fast · Wan 2.7\n"
            "  • Veo 3.1 Lite · Grok Imagine 1.5\n\n"
            "<b>🎬 Kling (حتى 4K):</b>\n"
            "  • Kling 3.0 · Kling O3\n\n"
            "<b>🏆 فيديو بريميوم (حتى 4K):</b>\n"
            "  • Veo 3.1 · Veo 3.1 Fast\n"
            "  • Sora 2 Pro\n\n"
            "<b>🎙 صوت</b>\n\n"
            "  ✕  الصور الرمزية\n\n"
            "  ⬆  الدقة: حتى 4K\n\n"
            "<b>💰 التسعير:</b>\n"
            "  ساعة   →  <b>{p1}◈</b>\n"
            "  ساعتان  →  <b>{p2}◈</b>  <i>(−10% في الساعة)</i>\n"
            "  3 ساعات  →  <b>{p3}◈</b>  <i>(−20% في الساعة)</i>"
        ),
        "unlim_tier_title": "⚡  <b>لا محدود {name}</b>",
        "unlim_info_tier_btn": "{emoji}  {name}  —  من {coins}◈",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    s = STR.get(lang, STR["en"]).get(key, STR["en"].get(key, key))
    return s.format(**kwargs) if kwargs else s


# ── Client reply-keyboard button labels (per language, with reverse lookup) ──
CLIENT_BUTTONS = {
    "main_menu": {"en": STR["en"]["menu_main_menu"], "ru": STR["ru"]["menu_main_menu"], "ar": STR["ar"]["menu_main_menu"]},
    "wallet":    {"en": STR["en"]["menu_wallet"],     "ru": STR["ru"]["menu_wallet"],     "ar": STR["ar"]["menu_wallet"]},
    "video":     {"en": STR["en"]["menu_video"],      "ru": STR["ru"]["menu_video"],      "ar": STR["ar"]["menu_video"]},
    "images":    {"en": STR["en"]["menu_images"],     "ru": STR["ru"]["menu_images"],     "ar": STR["ar"]["menu_images"]},
    "audio":     {"en": STR["en"]["menu_audio"],      "ru": STR["ru"]["menu_audio"],      "ar": STR["ar"]["menu_audio"]},
    "orders":    {"en": STR["en"]["menu_orders"],     "ru": STR["ru"]["menu_orders"],     "ar": STR["ar"]["menu_orders"]},
    "support":   {"en": STR["en"]["menu_support"],    "ru": STR["ru"]["menu_support"],    "ar": STR["ar"]["menu_support"]},
}

CLIENT_ACTION_BY_TEXT = {
    label: action
    for action, labels in CLIENT_BUTTONS.items()
    for label in labels.values()
}

CLIENT_TEXTS = set(CLIENT_ACTION_BY_TEXT.keys())
