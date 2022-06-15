package io.github.kiemlicz

import monix.eval.Task
import monix.execution.Scheduler

import java.security.SecureRandom
import scala.annotation.tailrec

object Stress {
  val rand = new SecureRandom()
  @volatile
  var blackhole: Double = _

  private def load(): Unit = {
    println(s"load() running in thread: ${Thread.currentThread().getName}")

    @tailrec
    def go(i: Int = 1): Unit = {
      blackhole = List.fill(i)(rand.nextDouble()).product
      println(
        s"""
      Thread name: ${Thread.currentThread().getName}
      Avail CPU: ${Runtime.getRuntime.availableProcessors()}
      """
      )
      go(i + 1)
    }

    go()
  }

  def main(args: Array[String]): Unit = {
    implicit val sched: Scheduler = Scheduler.forkJoin(16, 128)

    println("Start main")

    val t: Task[Unit] = Task {
      load()
    }.executeAsync

    List.fill(100)(t).foreach { e =>
      e.runAsyncAndForget(sched)
      Thread.sleep(5000)
    }

    Thread.sleep(3600 * 100)
    println("End main")
  }
}
