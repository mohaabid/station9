// A bot player driven over TCP (one JSON command per line) so tests can play the map.
const mineflayer = require('mineflayer')
const net = require('net')
const { Vec3 } = require('vec3')

const log = []
const bot = mineflayer.createBot({ host: '127.0.0.1', port: 25565, username: process.argv[2] || 'Tester', version: '1.20.4' })
const flat = c => { try { return typeof c === 'string' ? c : (c.toString ? c.toString() : JSON.stringify(c)) } catch (e) { return String(c) } }
bot.on('messagestr', m => log.push({ t: Date.now(), kind: 'chat', text: m }))
bot.on('title', (t, type) => log.push({ t: Date.now(), kind: 'title_' + type, text: JSON.stringify(t) }))
bot.on('actionBar', t => log.push({ t: Date.now(), kind: 'actionbar', text: flat(t) }))
bot.on('soundEffectHeard', (name, pos, vol, pitch) => log.push({ t: Date.now(), kind: 'sound', text: name, pos, vol, pitch }))
bot.on('hardcodedSoundEffectHeard', (id, cat, pos, vol, pitch) => log.push({ t: Date.now(), kind: 'sound', text: 'id:' + id, pos }))
bot.on('death', () => log.push({ t: Date.now(), kind: 'death' }))
bot.on('kicked', r => { console.log('KICKED', r); process.exit(1) })
bot.on('error', e => console.log('ERR', e.message))
bot._client.on('named_sound_effect', p => log.push({ t: Date.now(), kind: 'sound', text: p.soundName }))
bot._client.on('sound_effect', p => { if (p.soundEvent && p.soundEvent.resource) log.push({ t: Date.now(), kind: 'sound', text: p.soundEvent.resource }) })

const sleep = ms => new Promise(r => setTimeout(r, ms))

async function walkTo (x, z, opts = {}) {
  const tol = opts.tol || 0.35
  const timeout = Date.now() + (opts.timeout || 30000)
  bot.setControlState('sprint', !!opts.sprint)
  bot.setControlState('sneak', !!opts.sneak)
  let stuck = 0; let last = bot.entity.position.clone()
  while (Date.now() < timeout) {
    const p = bot.entity.position
    const dx = x - p.x; const dz = z - p.z
    if (Math.hypot(dx, dz) < tol) break
    await bot.lookAt(new Vec3(x, p.y + 1.6, z), true)
    bot.setControlState('forward', true)
    bot.setControlState('jump', !!opts.jump)
    await sleep(50)
    if (p.distanceTo(last) < 0.01) { stuck++ } else { stuck = 0 }
    last = p.clone()
    if (stuck > 30) { bot.setControlState('jump', true); await sleep(250); bot.setControlState('jump', false); stuck = 0 }
  }
  bot.clearControlStates()
  const p = bot.entity.position
  return { x: p.x, y: p.y, z: p.z, ok: Math.hypot(x - p.x, z - p.z) < tol + 0.3 }
}

async function handle (cmd) {
  switch (cmd.op) {
    case 'pos': { const p = bot.entity.position; return { x: p.x, y: p.y, z: p.z, yaw: bot.entity.yaw, pitch: bot.entity.pitch, hp: bot.health } }
    case 'log': { const out = log.splice(0, log.length); return out }
    case 'walk': return await walkTo(cmd.x, cmd.z, cmd)
    case 'route': { let r; for (const [x, z] of cmd.points) { r = await walkTo(x, z, cmd); if (!r.ok) return r } return r }
    case 'lookat': await bot.lookAt(new Vec3(cmd.x, cmd.y, cmd.z), true); return { ok: true }
    case 'look': await bot.look(cmd.yaw, cmd.pitch, true); return { ok: true }
    case 'use_block': {
      const b = bot.blockAt(new Vec3(cmd.x, cmd.y, cmd.z))
      if (!b) return { ok: false, err: 'no block' }
      await bot.lookAt(b.position.offset(0.5, 0.5, 0.5), true)
      try { await bot.activateBlock(b) } catch (e) { return { ok: false, err: e.message } }
      return { ok: true, name: b.name }
    }
    case 'use_item': bot.activateItem(); await sleep(100); bot.deactivateItem(); return { ok: true }
    case 'hold': {
      const it = bot.inventory.items().find(i => i.name === cmd.name)
      if (!it) return { ok: false, err: 'not in inventory' }
      await bot.equip(it, 'hand'); return { ok: true }
    }
    case 'inv': return bot.inventory.items().map(i => ({ name: i.name, count: i.count, slot: i.slot }))
    case 'open_take': {  // open a container and take everything
      const b = bot.blockAt(new Vec3(cmd.x, cmd.y, cmd.z))
      const win = await bot.openContainer(b)
      const got = []
      for (const it of win.containerItems()) { await win.withdraw(it.type, null, it.count); got.push(it.name) }
      win.close(); return { ok: true, got }
    }
    case 'controls': for (const [k, v] of Object.entries(cmd.set)) bot.setControlState(k, v); return { ok: true }
    case 'sleep': await sleep(cmd.ms); return { ok: true }
    case 'block': { const b = bot.blockAt(new Vec3(cmd.x, cmd.y, cmd.z)); return b ? { name: b.name, props: b.getProperties() } : null }
    default: return { err: 'unknown op ' + cmd.op }
  }
}

bot.once('spawn', () => {
  const server = net.createServer(sock => {
    let buf = ''
    sock.on('data', async d => {
      buf += d
      let i
      while ((i = buf.indexOf('\n')) >= 0) {
        const line = buf.slice(0, i); buf = buf.slice(i + 1)
        let res
        try { res = await handle(JSON.parse(line)) } catch (e) { res = { err: e.message } }
        sock.write(JSON.stringify(res) + '\n')
      }
    })
  })
  server.listen(25590, '127.0.0.1', () => console.log('DRIVER READY'))
})
